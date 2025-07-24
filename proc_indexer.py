 
#This code is just an attempt at experimentation with developing a utility with which we can index the stored procedures in sybase database
__author__="Adarsh Naik "
__status__="Development"
__date__="23-07-2025"
import logging
logging.basicConfig(level=logging.INFO)
import json
from antlr4 import *
from TSqlLexer import TSqlLexer
from TSqlParser import TSqlParser
from TSqlParserListener import TSqlParserListener
import os

class ProcedureIndexer(TSqlParserListener):
    def __init__(self):
        self.current_proc = None
        self.index = {}

    def enterCreate_or_alter_procedure(self, ctx):
        # Extract procedure name
        proc_name = ctx.func_proc_name_schema().getText().lower()
        self.current_proc = proc_name
        self.index[proc_name] = {"params": [], "calls": [], "tables": []}

        # Extract parameters
        param_list_ctx = ctx.procedure_param()
        if param_list_ctx:
            for param in param_list_ctx:
                param_text = param.getText()
                self.index[proc_name]["params"].append(param_text)

    def enterExecute_statement(self, ctx):
        if self.current_proc:
            try:
                called_proc = ctx.func_proc_name_server_database_schema().getText().lower()
                self.index[self.current_proc]["calls"].append(called_proc)
            except:
                pass  # In some cases, proc name might be different (handle later)

    def enterInsert_statement(self, ctx):
        if self.current_proc:
            table = ctx.ddl_object().getText().lower()
            self.index[self.current_proc]["tables"].append(table)

    def enterUpdate_statement(self, ctx):
        if self.current_proc:
            table = ctx.ddl_object().getText().lower()
            self.index[self.current_proc]["tables"].append(table)

    def enterDelete_statement(self, ctx):
        if self.current_proc:
            table = ctx.delete_statement_from().ddl_object().getText().lower()
            self.index[self.current_proc]["tables"].append(table)

    def enterSelect_statement_standalone(self, ctx):
        if self.current_proc:
            try:
                from_clause = ctx.select_statement().query_expression().query_specification().table_sources()
                if from_clause:
                    for ts in from_clause.table_source():
                        table = ts.table_source_item().full_table_name().getText().lower()
                        self.index[self.current_proc]["tables"].append(table)
            except:
                pass  # Some selects may not have full context

    def get_index(self):
        # Remove duplicates
        for proc in self.index.values():
            proc["params"] = list(set(proc["params"]))
            proc["calls"] = list(set(proc["calls"]))
            proc["tables"] = list(set(proc["tables"]))
        return self.index


def main():
    input_file = "test.sql"
    input_stream = FileStream(input_file, encoding='utf-8')
    lexer = TSqlLexer(input_stream)
    tokens = CommonTokenStream(lexer)
    parser = TSqlParser(tokens)
    tree = parser.tsql_file()
    print(tree.toStringTree(recog=parser))


    walker = ParseTreeWalker()
    listener = ProcedureIndexer()
    walker.walk(listener, tree)

    with open("index.json", "w") as f:
        json.dump(listener.get_index(), f, indent=2)

if __name__ == "__main__":
    main()






