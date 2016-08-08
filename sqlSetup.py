# -*- coding: utf-8 -*-
"""
Created on Tue May 24 16:14:19 2016

@author: Raunak Mundada
"""
from __future__ import print_function

import mysql.connector
from mysql.connector import errorcode
from mysql.connector import Error
from collections import OrderedDict
import pandas as pd


DB_NAME = 'Olympics'

TABLES = OrderedDict()
def defineTables():
    TABLES['Country_Details'] = (
    "CREATE TABLE `Country_Details` ("
    "  `Author_Id` char(20) NOT NULL,"
    "  `Author_Name` varchar(255) NOT NULL,"
    "  `Author_Affiliation` varchar(255),"
    "  `Author_Email` varchar(255),"
    "  `Author_Interests` text(21845),"
    "  `Author_Cited_By` int,"
    "  `Author_hIndex` int,"
    "  `Author_i10Index` int,"
    "  `Author_hIndex_recent` int,"
    "  `Author_i10Index_recent` int,"
    "  PRIMARY KEY (`Author_Id`)"
    ") ENGINE=InnoDB")

    TABLES['Publishing_Detail'] = (
    "CREATE TABLE `Publishing_Detail` ("
    " `Pub_Id` varchar(255) NOT NULL,"
    " `Pub_Title` text(21845),"
    " `Pub_Authors` text(21845),"
    " `Pub_Publisher` text(21845),"
    " `Pub_Journal` text(21845),"
    " `Pub_Abstract` text(21845),"
    " `Pub_Volume` char(20),"
    " `Pub_Year` int,"
    " `Pub_Citedby` int,"
    " `Pub_URL` text(21845),"
    " `Author_Id` char(20) NOT NULL,"
    " PRIMARY KEY (`Pub_Id`),"
    " CONSTRAINT FOREIGN KEY (`Author_Id`) REFERENCES `Author`(`Author_Id`) ON DELETE CASCADE"
    ") ENGINE = InnoDB")

    return TABLES
