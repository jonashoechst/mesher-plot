import csv, os

def csvs_from_folder(folder):
    colletion = []
    for root, dirs, files in os.walk(folder):
        if len(files) == 0:
            print("Read no files. Sure this is the right folder? Aborting.")
            sys.exit(1)
        for f in sorted(files):
            csv = CSVObject(os.path.join(root, f))
            colletion.append(csv)
    return colletion

class CSVObject():
    def __init__(self, filepath, quotechar='\''):
        self.filepath = filepath
        self.filename = os.path.basename(filepath)
        with open(filepath, "rb") as f:
            reader = csv.reader(f, quotechar=quotechar)
            try:
                self.header = reader.next()
                self.rows = [x for x in reader]

                # Sometimes it happens, that a value in a row is empty. We remove them.
                for row in self.rows:
                    for val in row:
                        if val == '':
                            self.rows.remove(row)

                # iterate through rows and convert numbers to floats or ints.
                for row_number in range(len(self.header)):
                    for row in self.rows:
                        try:
                            if float(row[row_number]).is_integer():
                                row[row_number] = int(float(row[row_number]))
                            else:
                                row[row_number] = float(row[row_number])
                        except ValueError:
                            pass

                # Transform rows to columns.
                self.columns = []
                for row_number in range(len(self.header)):
                    column = []
                    for row in self.rows: column.append(row[row_number])
                    self.columns.append(column)

                # Create a dict from two lists.
                self.dict_log = dict(zip(self.header, self.columns))
                self.row_dict = [dict(zip(self.header, r)) for r in self.rows]
            except:
                print("Error parsing csv: "+self.filepath)
                raise

    def is_empty(self):
        if len(self.rows) < 1:
            return True
        else:
            return False

    def get_values(self, key): return self.dict_log[key]

    def get_diff_time(self, first_col, second_col):
        values = []
        if type(first_col) is int and type(second_col) is int:
            for row in self.rows:
                values.append(int(row[first_col]) - int(row[second_col]))
        if type(first_col) is str and type(second_col) is str:
            for row in self.row_dict:
                values.append(int(row[first_col]) - int(row[second_col]))
        return values

    def get_values_normalized(self, key, timestamp_start, timestamp_end, ts_rowname="timestamp_ms", ts_fraction=1000, value_factor=1.0):
        values = []

        last_timestamp = timestamp_start - 1
        for row in self.row_dict:
            timestamp = int(row[ts_rowname]/ts_fraction)

            # ignore all ts outside the interval
            if timestamp < timestamp_start: continue
            if timestamp >= timestamp_end: continue

            # ignore doubled timestamps
            if last_timestamp >= timestamp:
                #print(str(last_timestamp)+" ("+str(last_timestamp-timestamp_start)+") is doubled in "+self.filename)
                continue

            # fill leftout timestamps
            while last_timestamp < timestamp - 1:
                # pad with previous value
                values.append(values[-1]) if len(values) > 0 else values.append(0);
                last_timestamp += 1
                # print(str(last_timestamp)+" ("+str(last_timestamp-timestamp_start)+") was padded for "+self.filename)

            # append value
            try:
                values.append(row[key] * value_factor)
            except(TypeError):
                print "key: " + key + " value: " + row[key]
                values.append(row[key])
            last_timestamp = timestamp

        values.extend([0] * (timestamp_end - last_timestamp))
        return values

        def get_row_dict_by_value(self, column, value):
            for row in self.row_dict:
                if row[column] == value: return row

            return None


if __name__ == "__main__":
    obj = CSVObject("csvobject-test.csv")
    print("header: \n  "+str(obj.header))

    print("\nrows: ")
    for row in obj.rows:
        print("  "+str(row))

    print("\ncolumns: ")
    for col in obj.columns:
        print("  "+str(col))

    print("\ndict_log: (array per column)")
    for key in obj.dict_log:
        print "  "+str(key) + ': ' + str(obj.dict_log[key])

    print("\nrow_dict: (dict per row)")
    for row in obj.row_dict:
        print("  "+str(row))
