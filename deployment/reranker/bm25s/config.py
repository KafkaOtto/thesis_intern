import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

import Stemmer

stemmer = Stemmer.Stemmer("english")