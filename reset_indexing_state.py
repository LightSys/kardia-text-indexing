import data_access
import os

data_accessor = data_access.MySQLDataAccessor()
data_accessor.delete_all_index_data()
if os.path.exists('index_events'):
    os.remove('index_events')
