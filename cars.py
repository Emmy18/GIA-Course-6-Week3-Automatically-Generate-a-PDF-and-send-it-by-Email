#!/usr/bin/env python3

import json
import os
import locale
import sys
from reports import generate as gen_report
from emails import generate as gen_email
from emails import send as send_email


def load_data(filename):
  """Loads the contents of filename as a JSON file."""
  with open(filename) as json_file:
    data = json.load(json_file)
  return data


def format_car(car):
  """Given a car dictionary, returns a nicely formatted name."""
  return "{} {} ({})".format(
      car["car_make"], car["car_model"], car["car_year"])


def process_data(data):
  """Analyzes the data, looking for maximums.

  Returns a list of lines that summarize the information.
  """
  max_revenue = {"revenue": 0}
  max_sales = {"total_sales": 0}
  most_popular_cars = {}

  for item in data:
    # Calculate the revenue generated by this model (price * total_sales)
    # We need to convert the price from "$1234.56" to 1234.56
    item_price = locale.atof(item["price"].strip("$"))
    item_revenue = item["total_sales"] * item_price
    if item_revenue > max_revenue["revenue"]:
      item["revenue"] = item_revenue
      max_revenue = item
    # TODO: also handle max sales
    item_sales = item["total_sales"] 
    if item_sales > max_sales["total_sales"]:
      item["total_sales"] = item_sales
      max_sales = item
    # TODO: also handle most popular car_year
    i = item["car"]["car_year"]
    if i in most_popular_cars.keys():
            most_popular_cars[i] += item["total_sales"]
    else: most_popular_cars[i] = item["total_sales"]
    most_popular_cars_values = most_popular_cars.values()
    max_value = max(most_popular_cars_values)
    max_year = max(most_popular_cars, key=most_popular_cars.get)

  summary = [
    "The {} generated the most revenue: ${}".format(
      format_car(max_revenue["car"]), max_revenue["revenue"]),
    "The {} has the most sales: {}". format(format_car(max_sales["car"]), max_sales["total_sales"]),
    "The most popular year was {} with {} sales.".format(max_year, max_value)
  ]

  return summary


def cars_dict_to_table(car_data):
  """Turns the data in car_data into a list of lists."""
  table_data = [["ID", "Car", "Price", "Total Sales"]]
  for item in car_data:
    table_data.append([item["id"], format_car(item["car"]), item["price"], item["total_sales"]])
  return table_data


def main(argv):
  """Process the JSON data and generate a full report out of it."""
  data = load_data("/home/student-01-9a4eceed29d8/car_sales.json")
  summary = process_data(data)
  summary = "\n".join(summary)
  print(summary)
  # TODO: turn this into a PDF report
  gen_report("/tmp/cars.pdf", "Cars Report", summary, cars_dict_to_table(data))
  # TODO: send the PDF report as an email attachment
  mesg = gen_email("automation@example.com", "{}@example.com".format(os.environ.get('USER')), "Sales summary for last month", summary, "/tmp/cars.pdf")
  send_email(mesg)

if __name__ == "__main__":
  main(sys.argv)
