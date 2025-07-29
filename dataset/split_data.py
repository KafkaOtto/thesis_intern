import logging
import random
import bz2

# Configure logging with thread safety
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(threadName)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


input_file = "myown/input/crag_task_1_and_2_dev_v4.jsonl.bz2"
test_output_file = "myown/input/crag_task_1_and_2_dev_v4_warmup.jsonl.bz2"
train_output_file = "myown/input/crag_task_1_and_2_dev_v4_prod.jsonl.bz2"
with bz2.open(input_file, 'rt', encoding='utf-8') as f:
    lines = f.readlines()
print(f"lines size: {len(lines)}")
random.shuffle(lines)
test_lines = lines[:100]
train_lines = lines[100:]

# with bz2.open(test_output_file, 'wt', encoding='utf-8') as f:
#    for line in test_lines:
#        f.write(line)

# Step 5: Save train file (compressed)
# with bz2.open(train_output_file, 'wt', encoding='utf-8') as f:
#    for line in train_lines:
#        f.write(line)
