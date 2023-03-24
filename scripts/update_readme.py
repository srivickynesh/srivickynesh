import random

# Define the list of quotes
QUOTES = [
    "The best way to predict your future is to create it. - Abraham Lincoln",
    "In the end, we only regret the chances we didn't take. - Lewis Carroll",
    "Success is not final, failure is not fatal: it is the courage to continue that counts. - Winston Churchill",
    # Add more quotes here
]

# Read the existing contents of the README file
with open('README.md', 'r') as f:
    contents = f.read()

# Find the position of the first section and insert the quote after it
pos = contents.find('\n##')
if pos >= 0:
    quote = random.choice(QUOTES)
    new_contents = contents[:pos+2] + f'\n> {quote}\n\n' + contents[pos+2:]
else:
    quote = random.choice(QUOTES)
    new_contents = f'\n> {quote}\n\n' + contents

# Write the updated contents back to the README file
with open('README.md', 'w') as f:
    f.write(new_contents)
