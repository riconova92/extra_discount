# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "extra_discount"
app_title = "Extra Discount"
app_publisher = "PT DAS"
app_description = "extra discount"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "digitalasiasolusindo@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/extra_discount/css/extra_discount.css"
# app_include_js = "/assets/extra_discount/js/extra_discount.js"

# include js, css files in header of web template
# web_include_css = "/assets/extra_discount/css/extra_discount.css"
# web_include_js = "/assets/extra_discount/js/extra_discount.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "extra_discount.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "extra_discount.install.before_install"
# after_install = "extra_discount.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "extra_discount.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Sales Invoice" : {
		"validate" : "extra_discount.custom_method_extra_discount.calculate_extra_discount"
	}
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"extra_discount.tasks.all"
# 	],
# 	"daily": [
# 		"extra_discount.tasks.daily"
# 	],
# 	"hourly": [
# 		"extra_discount.tasks.hourly"
# 	],
# 	"weekly": [
# 		"extra_discount.tasks.weekly"
# 	]
# 	"monthly": [
# 		"extra_discount.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "extra_discount.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "extra_discount.event.get_events"
# }

