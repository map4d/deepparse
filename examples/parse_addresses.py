import pandas as pd

from deepparse import download_from_url
from deepparse.dataset_container import PickleDatasetContainer
from deepparse.parser import AddressParser

# Here is an example on how to parse multiple addresses
# First, let's download the train and test data from the public repository.
saving_dir = "./data"
file_extension = "p"
test_dataset_name = "predict"
download_from_url(test_dataset_name, saving_dir, file_extension=file_extension)

#  Now let's load the dataset using one of our dataset container
addresses_to_parse = PickleDatasetContainer("./data/predict.p", is_training_container=False)

# We can sneak peek some addresses
print(addresses_to_parse[:2])

# Let's use the BPEmb model on a GPU
address_parser = AddressParser(model_type="bpemb", device=0)

# We can now parse some addresses
parsed_addresses = address_parser(addresses_to_parse[0:300])

# When parsing addresses, some data quality tests are applied to the dataset.
# First, it validates that no addresses to parse are empty.
# Second, it validates that no addresses are whitespace-only.
# The next two lines are rising a DataError.
address_parser("")  # Raise an error
address_parser(" ")  # Raise an error

# We can also put our parsed address into a pandas dataframe for analysis
# You can choose the fields to use or use the default one
fields = ["StreetNumber", "StreetName", "Municipality", "Province", "PostalCode"]
parsed_address_data_frame = pd.DataFrame(
    [parsed_address.to_dict(fields=fields) for parsed_address in parsed_addresses],
    columns=fields,
)
