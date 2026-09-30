#!/usr/bin/env python3
"""
HomePulse Local Server & Live Redfin/Zillow Traversal Proxy
Serves index.html + data/listings.json and provides /api/traverse for live on-demand
Redfin GIS (MLS For-Sale) and Zillow/Redfin Rental scraping for any US coordinates & radius.
"""

import http.server
import json
import math
import socketserver
import urllib.parse
from scraper import fetch_region_sales, fetch_region_rentals

PORT = 8085


class HomePulseHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "no-cache")
        super().end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/api/traverse":
            qs = urllib.parse.parse_qs(parsed.query)
            try:
                lat = float(qs.get("lat", [37.3382])[0])
                lng = float(qs.get("lng", [-121.8863])[0])
                radius = float(qs.get("radius", [10])[0])
                name = qs.get("location", ["Custom Area"])[0]

                # Convert radius miles to bounding box degrees
                lat_deg = radius / 69.0
                lng_deg = radius / max(69.0 * math.cos(math.radians(lat)), 10.0)
                bbox = (
                    round(lng - lng_deg, 4),
                    round(lat - lat_deg, 4),
                    round(lng + lng_deg, 4),
                    round(lat + lat_deg, 4),
                )

                region = {
                    "name": name,
                    "center": [lat, lng],
                    "bbox": bbox,
                    "tax_rate": 0.0125,
                    "county": f"{name.split(',')[0]} County Assessor",
                    "seismic": "Standard Regional Seismic & Structural Code Zone",
                    "radon_avg": "1.4 pCi/L (EPA Regional Baseline)",
                    "buy_limit": 60,
                    "rent_limit": 35,
                }

                sales, median_psqft = fetch_region_sales(region)
                rentals = fetch_region_rentals(region, median_psqft)
                combined = sales + rentals

                body = json.dumps({
                    "status": "ok",
                    "count": len(combined),
                    "listings": combined,
                }).encode("utf-8")

                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
            except Exception as e:
                err = json.dumps({"status": "error", "message": str(e)}).encode("utf-8")
                self.send_response(500)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(err)
            return

        return super().do_GET()


if __name__ == "__main__":
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("0.0.0.0", PORT), HomePulseHandler) as httpd:
        print(f"HomePulse server listening on http://0.0.0.0:{PORT}")
        httpd.serve_forever()
