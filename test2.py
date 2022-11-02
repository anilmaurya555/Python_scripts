# -*- coding: utf-8 -*-
"""
Created on Tue Jul 20 13:43:19 2021

@author: AMAURYA
"""

math_marks = float(input("Enter the MCQ marks: "))
theory_marks = float(input("Enter the Theory marks: "))


english_mark = float(input("enter engish marks: "))
if (math_marks >=40 and theory_marks >=30) or (math_marks + theory_marks) >=70 :

    print("\nYou have passed")
else:
    print("\nYou have failed")