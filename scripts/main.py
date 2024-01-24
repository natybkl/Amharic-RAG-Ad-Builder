import os
import json
import re
import zipfile
import csv
import pandas as pd
from utils import Util
import clean, parse, utils
import subprocess


if __name__ == "__main__":
    subprocess.run(["python", "parse.py"])
    subprocess.run(["python", "clean.py"])
