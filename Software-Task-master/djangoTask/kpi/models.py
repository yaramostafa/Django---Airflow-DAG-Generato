from django.db import models
import json
# import sqlite3
# Create your models here.
# def get_asset_ids():
#     # Open a connection to the database
#     conn = sqlite3.connect('../processed_data.db')  # Adjust path if needed
#     cursor = conn.cursor()
#
#     # Fetch unique asset_id values from the processed_data table
#     cursor.execute("SELECT DISTINCT asset_id FROM processed_data")
#     asset_ids = [row[0] for row in cursor.fetchall()]
#
#     # Close the connection
#     conn.close()
#
#     return [(asset_id, asset_id) for asset_id in asset_ids]


def get_asset_ids():
    """
    Reads unique asset IDs from a text file containing JSON-like data.

    Returns:
        list: A list of tuples where each tuple contains an asset ID twice.
    """
    file_path = "data.txt"

    with open(file_path, 'r') as file:
        # Parse each line as JSON and collect unique asset_ids
        asset_ids = set(json.loads(line.strip())['asset_id'] for line in file if line.strip())

    # Return asset IDs in the desired format
    return [(asset_id, asset_id) for asset_id in asset_ids]


class KPI(models.Model):
    name = models.CharField(max_length=255)
    expression = models.TextField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class AssetKPI(models.Model):
    asset_id = models.CharField(max_length=255, choices=get_asset_ids())
    kpi = models.ForeignKey(KPI, related_name="assets", on_delete=models.CASCADE)

    def __str__(self):
        return f"Asset {self.asset_id} linked to {self.kpi.name}"
