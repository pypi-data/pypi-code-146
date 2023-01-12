# Generated from winval.g4 by ANTLR 4.10.1
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .winvalParser import winvalParser
else:
    from winvalParser import winvalParser

# This class defines a complete generic visitor for a parse tree produced by winvalParser.

class winvalVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by winvalParser#constraint.
    def visitConstraint(self, ctx:winvalParser.ConstraintContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by winvalParser#AccessExpr.
    def visitAccessExpr(self, ctx:winvalParser.AccessExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by winvalParser#StringExpr.
    def visitStringExpr(self, ctx:winvalParser.StringExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by winvalParser#BoolExpr.
    def visitBoolExpr(self, ctx:winvalParser.BoolExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by winvalParser#FloatExpr.
    def visitFloatExpr(self, ctx:winvalParser.FloatExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by winvalParser#SetExpr.
    def visitSetExpr(self, ctx:winvalParser.SetExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by winvalParser#VariableExpr.
    def visitVariableExpr(self, ctx:winvalParser.VariableExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by winvalParser#IntExpr.
    def visitIntExpr(self, ctx:winvalParser.IntExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by winvalParser#ListExpr.
    def visitListExpr(self, ctx:winvalParser.ListExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by winvalParser#EmptySetExpr.
    def visitEmptySetExpr(self, ctx:winvalParser.EmptySetExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by winvalParser#ParenExpr.
    def visitParenExpr(self, ctx:winvalParser.ParenExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by winvalParser#InfixExpr.
    def visitInfixExpr(self, ctx:winvalParser.InfixExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by winvalParser#PrefixExpr.
    def visitPrefixExpr(self, ctx:winvalParser.PrefixExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by winvalParser#VariableExpr2.
    def visitVariableExpr2(self, ctx:winvalParser.VariableExpr2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by winvalParser#elements.
    def visitElements(self, ctx:winvalParser.ElementsContext):
        return self.visitChildren(ctx)



del winvalParser