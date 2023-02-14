TRANSACTION_TYPES_TO_KEEP = ['Sent P2P', 'Received P2P', 'Cash Card Debit']
COLUMNS_TO_KEEP = ['Date', 'Net Amount', 'Name of sender/receiver']
TRANSACTION_TYPES_TO_COPY_NOTES = ['Cash Card Debit']

import pandas

def process_csv(
	input_file: str,
	output_file: str,
	transactions_types_to_keep: str,
	columns_to_keep: str,
	transaction_types_to_copy_notes: str,
	start_date: str = None,
	end_date: str = None
	):

	def transform_row(r):
		n = r.copy()
		if n['Transaction Type'] in transaction_types_to_copy_notes:
			n['Name of sender/receiver'] = n['Notes']
		return n

	df = pandas.read_csv(input_file, index_col='Transaction ID', parse_dates=['Date'])

	# Filter dates (format: yyyy-MM-dd)
	if start_date:
		df = df[df.Date >= start_date]
	if end_date:
		df = df[df.Date <= end_date]

	# Filter transaction types
	df = df[df['Transaction Type'].isin(transactions_types_to_keep)]

	# Copy notes to name of sender/receiver
	df = df.transform(transform_row, axis = 1)

	# Filter columns
	df = df[columns_to_keep]

	# Change date format
	df.Date = df.Date.dt.strftime('%Y-%m-%d')

	# Rename columns
	df = df.rename(columns={'Net Amount': 'Amount', 'Name of sender/receiver': 'Description'})

	df.to_csv(output_file, index = False)

if __name__ == "__main__":

	import argparse

	parser = argparse.ArgumentParser(description='Process transactions CSV from Square Cash for import into Wave accounting software.')
	parser.add_argument('input_file', type = str, help = 'the input file (comma-separated values)')
	parser.add_argument('output_file', type = str, help = 'the output file (comma-separated values)')
	parser.add_argument('--start_date', type = str, help = 'the start date for transactions to keep (yyyy-MM-dd)')
	parser.add_argument('--end_date', type = str, help = 'the end date for transactions to keep (yyyy-MM-dd)')
	args = parser.parse_args()

	process_csv(
		args.input_file,
		args.output_file,
		TRANSACTION_TYPES_TO_KEEP,
		COLUMNS_TO_KEEP,
		TRANSACTION_TYPES_TO_COPY_NOTES,
		args.start_date,
		args.end_date
		)
