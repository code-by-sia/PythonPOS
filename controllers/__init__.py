#  IoC
from common.controller import Controller
from common.report import Report

print("Registering controllers started:\n")
import controllers.basicInfo
import controllers.authentication 
import controllers.confirm 
import controllers.container 
import controllers.costs 
import controllers.dashboard 
import controllers.purchase 
import controllers.sales 
import controllers.system 
import controllers.testDev

print("\n\nRegistering reports started:\n")
import controllers.reports.cost
import controllers.reports.installment
import controllers.reports.order
import controllers.reports.sale
import controllers.reports.saleList
import controllers.reports.storage

print("\n\n")