# -*- coding: utf-8 -*-
# Copyright (c) 2015, Myme and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
import os
import requests
import json
import subprocess
from frappe.utils.background_jobs import enqueue
import re


from frappe import _, scrub
from frappe.utils import cint, flt, round_based_on_smallest_currency_fraction
from erpnext.controllers.accounts_controller import validate_conversion_rate, \
	validate_taxes_and_charges, validate_inclusive_tax


class custom_method_extra_discount(Document):
	pass




@frappe.whitelist(allow_guest=True)
def calculate_extra_discount(doc, method):

	# doc = frappe.get_doc("Sales Invoice", docname)
	additional_discount = 0
	if doc.taxes :

		cek_include = 0
		additional_discount = 0

		itemised_tax = get_itemised_tax(doc.taxes)
		itemised_taxable_amount = get_itemised_taxable_amount(doc.items)

		total_amount_dan_tax = frappe._dict()


		temp = 0
		ekstra_diskon = 0
		total_ekstra_diskon = 0
		for i in doc.items :
			temp = 0
			if i.extra_discount :
				ekstra_diskon = i.extra_discount

				for t in doc.taxes :

					if t.charge_type == "On Net Total" :
						if t.included_in_print_rate == 1 :
							temp += float(itemised_taxable_amount[i.item_code])

						else :
							temp += float(itemised_taxable_amount[i.item_code])
							total_amount_dan_tax = itemised_tax[i.item_code][t.description]
							temp += float(total_amount_dan_tax["tax_amount"] )

					else :
						temp += float(itemised_taxable_amount[i.item_code])
						total_amount_dan_tax = itemised_tax[i.item_code][t.description]
						temp += float(total_amount_dan_tax["tax_amount"] )
					

				total_ekstra_diskon = total_ekstra_diskon + (temp * ekstra_diskon / 100)


		additional_discount = total_ekstra_diskon
		doc.tes_field = additional_discount
		doc.discount_amount = additional_discount
		doc.base_discount_amount = additional_discount
		doc.apply_discount_on = "Grand Total"

		doc.calculate_taxes_and_totals()

	else :
		additional_discount = 0

		temp = 0
		ekstra_diskon = 0
		total_ekstra_diskon = 0

		for i in doc.items :
			if i.extra_discount :
				total_ekstra_diskon = total_ekstra_diskon + (i.amount * i.extra_discount / 100)

		additional_discount = total_ekstra_diskon
		doc.tes_field = additional_discount
		doc.discount_amount = additional_discount
		doc.base_discount_amount = additional_discount
		doc.apply_discount_on = "Grand Total"

		doc.calculate_taxes_and_totals()




@frappe.whitelist(allow_guest=True)
def get_itemised_tax(taxes):
	itemised_tax = {}
	for tax in taxes:
		if getattr(tax, "category", None) and tax.category=="Valuation":
			continue

		item_tax_map = json.loads(tax.item_wise_tax_detail) if tax.item_wise_tax_detail else {}
		if item_tax_map:
			for item_code, tax_data in item_tax_map.items():
				itemised_tax.setdefault(item_code, frappe._dict())

				if isinstance(tax_data, list):
					itemised_tax[item_code][tax.description] = frappe._dict(dict(tax_rate=flt(tax_data[0]),tax_amount=flt(tax_data[1])))
				else:
					itemised_tax[item_code][tax.description] = frappe._dict(dict(tax_rate=flt(tax_data),tax_amount=0.0))

	return itemised_tax


@frappe.whitelist(allow_guest=True)
def get_itemised_taxable_amount(items):
	itemised_taxable_amount = frappe._dict()
	for item in items:
		item_code = item.item_code or item.item_name
		itemised_taxable_amount.setdefault(item_code, 0)
		itemised_taxable_amount[item_code] += item.amount

	return itemised_taxable_amount






@frappe.whitelist(allow_guest=True)
def ding():
	return "dong"



@frappe.whitelist(allow_guest=True)
def check_invoice_outstanding(doc, method):

	# 
	for i in doc.references :
		# frappe.throw(i.reference_name)
		
		if i.allocated_amount > 0 :
			if i.reference_doctype == "Sales Invoice" or i.reference_doctype == "Purchase Invoice" :
				doc_reference = frappe.get_doc(i.reference_doctype, i.reference_name)

				if doc_reference.outstanding_amount <= 0 :
					frappe.throw("Invoice "+str(i.reference_name)+" already paid ")

	# 




@frappe.whitelist(allow_guest=True)
def reduce_days_active_user():
	
	cari_user = frappe.db.sql(""" SELECT pu.`name` FROM `tabPurchase User` pu WHERE pu.`enabled` = 1 """, as_list=1)

	if cari_user :
		for i in cari_user :
			purchase_user = frappe.get_doc("Purchase User", i[0])
			current_days = purchase_user.days_active - 1
			purchase_user.days_active = current_days
			# purchase_user.flags.ignore_permissions = True
			purchase_user.save(ignore_permissions=True)



@frappe.whitelist(allow_guest=True)
def check_subdomain(subdomain):
	new_subdomain = subdomain.lower()

	cari_subdomain = frappe.db.sql(""" SELECT ms.`name` FROM `tabMaster Subdomain` ms WHERE ms.`subdomain` = "{}" """.format(new_subdomain))

	# frappe.throw(str(cari_subdomain))

	if cari_subdomain :
		return "sudah ada"
	else :
		return "belum ada"

@frappe.whitelist(allow_guest=True)
def check_lower_case_and_alphabet_only(subdomain):
	
	if re.match(r'^[a-zA-Z0-9_]+$', subdomain):
		return "bisa"
	else :
		return "tidak bisa"


@frappe.whitelist(allow_guest=True)
def submit_dokumen():
	
	dokumen_nomor = "STE-00182"

	get_dokumen = frappe.get_doc("Stock Entry",dokumen_nomor)
	get_dokumen.flags.ignore_permissions = True
	get_dokumen.submit()