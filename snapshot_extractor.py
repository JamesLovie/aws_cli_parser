# James Lovie 2019
# JSON Parser Function - For EC2 Snapshots.
import json
import subprocess
import pandas as pd

class SnapshotExtractor:
    def __init__(self, profile):
        self.profile = profile

    def run_command(self):
        # Run AWS cli command and parse json output.
        test = subprocess.Popen(["aws","ec2","describe-snapshots","--profile", self.profile], stdout=subprocess.PIPE)
        aws_output = test.communicate()[0]
        decoded = aws_output.decode("utf-8")
        data = json.loads(decoded)
        data_keys = data['Snapshots']

        # Lambda with Map function to iterate over dictionary and extract elements.
        descriptions = map(lambda x : x['Description'], data_keys)
        encrypted = map(lambda x : x['Encrypted'], data_keys)
        snapshotIDs = map(lambda x : x['SnapshotId'], data_keys)
        # Create dataframe for each element.
        df_descriptions = pd.DataFrame(descriptions)
        df_encrypted = pd.DataFrame(encrypted)
        df_snapshotIDs = pd.DataFrame(snapshotIDs)
        # Concatanate dataframes together into one single dataframe.
        df_merge = pd.concat([df_descriptions, df_encrypted, df_snapshotIDs], axis=1, ignore_index=True)
        df_merge.columns = ['Description', 'Encrypted', 'SnapshotID']
        df_merge.to_csv('snapshots.csv', mode='a', header=False)

def main():
    profile = 'jameslovieuser'
    snapshotextractor = SnapshotExtractor(profile)
    print('Running AWS cli command...')
    snapshotextractor.run_command()
    print('Snapshot CSV file has been saved to the drive.')

if __name__ == '__main__':
	main()