from html.parser import HTMLParser
from io import StringIO
import csv
from dateutil import parser
from datetime import datetime

class TableHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_td = False
        self.in_tr = False
        self.current_data = []
        self.rows = []
        self.data_collected = False

    def handle_starttag(self, tag, attrs):
        if tag == 'tr':
            self.in_tr = True
            self.current_data = []
        elif tag in ('td', 'th'):
            self.in_td = True
            self.data_collected = False  # Reset data collected flag

    def handle_endtag(self, tag):
        if tag == 'tr':
            self.in_tr = False
            self.rows.append(self.current_data)
        elif tag in ('td', 'th'):
            self.in_td = False
            if not self.data_collected:  # If no data was collected, append an empty string
                self.current_data.append('')
            self.data_collected = False  # Reset for the next cell

    def handle_data(self, data):
        if self.in_td:
            self.current_data.append(data.strip())
            self.data_collected = True  # Mark that data was collected for this cell

def html_table_to_csv(html_string):
    parser = TableHTMLParser()
    parser.feed(html_string)
    
    output = StringIO()
    csv_writer = csv.writer(output)
    csv_writer.writerows(parser.rows)
    
    return output.getvalue()

def extract_high_tide_info_with_day_and_utc(csv_string):
    # Prepare to read the input CSV string
    input_csv = StringIO(csv_string)
    reader = csv.reader(input_csv)
    
    # Prepare to write the new CSV string
    output_csv = StringIO()
    fieldnames = ['High Tide Time', 'High Tide Value']
    writer = csv.DictWriter(output_csv, fieldnames=fieldnames)
    writer.writeheader()
    
    # Read the header row to find column indices
    headers = next(reader)
    day_index = headers.index('Day')
    high_tide_indices = [i for i, header in enumerate(headers) if 'High' in header]
    
    # Process each row in the input CSV
    for row in reader:
        day = row[day_index]  # Extract the day
        # Iterate over each "High" tide column using the identified indices
        for index in high_tide_indices:
            value = row[index]
            if value:  # Check if the cell is not empty
                # Extract time, UTC offset, and value for "High" tide
                parts = value.split(' ')
                time, ampm, utc_offset, value = parts[0], parts[1], parts[2], parts[3]
                # Append the day and UTC offset to the time
                time_with_day_and_utc = f"{day} {time} {ampm} {utc_offset}"
                # Write the extracted information to the new CSV
                writer.writerow({'High Tide Time': time_with_day_and_utc, 'High Tide Value': value})
    
    # Return the new CSV string
    return output_csv.getvalue()

def add_month_and_year_to_high_tide_info(csv_string, month, year):
    # Prepare to read the input CSV string
    input_csv = StringIO(csv_string)
    reader = csv.DictReader(input_csv)
    
    # Prepare to write the new CSV string
    output_csv = StringIO()
    fieldnames = ['High Tide Time', 'High Tide Value']
    writer = csv.DictWriter(output_csv, fieldnames=fieldnames)
    writer.writeheader()
    
    # Process each row in the input CSV
    for row in reader:
        # Extract the time and value for "High" tide
        high_tide_time = row['High Tide Time']
        high_tide_value = row['High Tide Value']
        # Insert the month and year to the time to produce a format of "DDD dd mmm yyyy hh:mm UTC"
        # Extract the day, time, and UTC offset from the time
        day, dd, time, ampm, utc_offset = high_tide_time.split(' ')
        # Append the month and year to the time
        time_with_month_and_year = f"{day} {month} {dd} {year} {time} {ampm} {utc_offset}"
        # parse the time to get the correct format
        time_with_month_and_year = parser.parse(time_with_month_and_year).strftime('%Y-%m-%d %H:%M %Z')
        # Write the updated information to the new CSV
        writer.writerow({'High Tide Time': time_with_month_and_year, 'High Tide Value': high_tide_value})
    
    # Return the new CSV string
    return output_csv.getvalue()

def extract_low_tide_info_with_day_and_utc(csv_string):
    # Prepare to read the input CSV string
    input_csv = StringIO(csv_string)
    reader = csv.reader(input_csv)
    
    # Prepare to write the new CSV string
    output_csv = StringIO()
    fieldnames = ['Low Tide Time', 'Low Tide Value']
    writer = csv.DictWriter(output_csv, fieldnames=fieldnames)
    writer.writeheader()
    
    # Read the header row to find column indices
    headers = next(reader)
    day_index = headers.index('Day')
    low_tide_indices = [i for i, header in enumerate(headers) if 'Low' in header]
    
    # Process each row in the input CSV
    for row in reader:
        day = row[day_index]  # Extract the day
        # Iterate over each "Low" tide column using the identified indices
        for index in low_tide_indices:
            value = row[index]
            if value:  # Check if the cell is not empty
                # Extract time, UTC offset, and value for "Low" tide
                parts = value.split(' ')
                time, ampm, utc_offset, value = parts[0], parts[1], parts[2], parts[3]
                # Append the day and UTC offset to the time
                time_with_day_and_utc = f"{day} {time} {ampm} {utc_offset}"
                # Write the extracted information to the new CSV
                writer.writerow({'Low Tide Time': time_with_day_and_utc, 'Low Tide Value': value})
    
    # Return the new CSV string
    return output_csv.getvalue()

def add_month_and_year_to_low_tide_info(csv_string, month, year):
    # Prepare to read the input CSV string
    input_csv = StringIO(csv_string)
    reader = csv.DictReader(input_csv)
    
    # Prepare to write the new CSV string
    output_csv = StringIO()
    fieldnames = ['Low Tide Time', 'Low Tide Value']
    writer = csv.DictWriter(output_csv, fieldnames=fieldnames)
    writer.writeheader()
    
    # Process each row in the input CSV
    for row in reader:
        # Extract the time and value for "Low" tide
        low_tide_time = row['Low Tide Time']
        low_tide_value = row['Low Tide Value']
        # Insert the month and year to the time to produce a format of "DDD dd mmm yyyy hh:mm UTC"
        # Extract the day, time, and UTC offset from the time
        day, dd, time, ampm, utc_offset = low_tide_time.split(' ')
        # Append the month and year to the time
        time_with_month_and_year = f"{day} {month} {dd} {year} {time} {ampm} {utc_offset}"
        # parse the time to get the correct format
        time_with_month_and_year = parser.parse(time_with_month_and_year).strftime('%Y-%m-%d %H:%M %Z')
        # Write the updated information to the new CSV
        writer.writerow({'Low Tide Time': time_with_month_and_year, 'Low Tide Value': low_tide_value})
    
    # Return the new CSV string
    return output_csv.getvalue()

def concatenate_csv_strings(csv_string1, csv_string2):
    # Convert CSV strings to file-like objects
    input_csv1 = StringIO(csv_string1)
    input_csv2 = StringIO(csv_string2)
    
    # Initialize CSV readers
    reader1 = csv.reader(input_csv1)
    reader2 = csv.reader(input_csv2)
    
    # Prepare to write the concatenated CSV string
    output_csv = StringIO()
    writer = csv.writer(output_csv)
    
    # Write the header from the first CSV string
    writer.writerow(next(reader1))
    
    # Write the rest of the rows from the first CSV string
    for row in reader1:
        writer.writerow(row)
    
    # Skip the header of the second CSV string
    next(reader2)
    
    # Write the rows from the second CSV string
    for row in reader2:
        writer.writerow(row)
    
    # Return the concatenated CSV string
    return output_csv.getvalue()

def extract_moon_phases(csv_string):
    # Initialize a StringIO object from the input CSV string
    csv_input = StringIO(csv_string)
    # Initialize a StringIO object for the output CSV string
    csv_output = StringIO()
    writer = csv.writer(csv_output)
    reader = csv.reader(csv_input)
    
    # Write the header for the output CSV
    writer.writerow(["Day", "Phase"])
    
    # Skip the header of the input CSV
    next(reader)
    
    # Iterate through each row of the input CSV
    for row in reader:
        day, phase = row[0], row[6]
        # Check if the phase is "New Moon" or "Full Moon"
        if phase in ["New Moon", "Full Moon"]:
            # Write the day and phase to the output CSV
            writer.writerow([day, phase])
    
    # Return the output CSV string
    return csv_output.getvalue()

def reformat_moon_dates(csv_string, month, year):
    # Initialize a StringIO object from the input CSV string
    csv_input = StringIO(csv_string)
    # Initialize a StringIO object for the output CSV string
    csv_output = StringIO()
    writer = csv.writer(csv_output)
    reader = csv.reader(csv_input)
    
    # Write the header for the output CSV
    writer.writerow(["Day", "Phase"])
    
    # Iterate through each row of the input CSV
    for row in reader:
        day, phase = row
        if day != "Day":  # Skip the header row
            # Parse the day and convert it to the desired format
            day_number = day.split()[1]  # Extract the day number
            # Construct the date string in the format YYYY-MM-DD
            date_str = f"{year}-{datetime.strptime(month, '%b').month:02d}-{int(day_number):02d}"
            # Write the reformatted date and phase to the output CSV
            writer.writerow([date_str, phase])
    
    # Return the output CSV string
    return csv_output.getvalue()