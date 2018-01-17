from rply import ParserGenerator, LexerGenerator
from rply.token import BaseBox

lg = LexerGenerator()
# Add takes a rule name, and a regular expression that defines the rule.
lg.add("PLUS", r"\+")
lg.add("MINUS", r"-")
lg.add("NUMBER", r"\d+")
lg.add("MULTIPLY", r"\*")
lg.add("DIVIDE", r"\/")
lg.add("MOD", r"%")
lg.add("OPEN_PAREN", r"\(")

lg.ignore(r"\s+")

lexer = lg.build()