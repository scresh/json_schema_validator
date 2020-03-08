from token_generator import TokenGenerator
from parser import Parser

file_content = open("exampleFile.txt").read()
token_generator = TokenGenerator(file_content)
parser = Parser(token_generator)
parser.start()