#!/usr/bin/env python3
"""Pesquisa leads empresariais usando Places API (New).

Requer GOOGLE_MAPS_API_KEY no ambiente. Não grava a chave em disco.
Uso:
  python google_places_leads.py "pousadas em São Sebastião SP" --limit 10 --out leads.json

Observação: Google Maps Platform é um serviço faturado. Use field masks mínimos e
revise os termos/licenças antes de armazenar ou redistribuir dados/fotos.
"""

import argparse
import json
import os
import sys
from pathlib import Path

import requests

SEARCH_URL = "https://places.googleapis.com/v1/places:searchText"

FIELDS = ",".join(
    [
        "places.id",
        "places.displayName",
        "places.formattedAddress",
        "places.primaryType",
        "places.rating",
        "places.userRatingCount",
        "places.websiteUri",
        "places.nationalPhoneNumber",
        "places.googleMapsUri",
        "places.photos",
    ]
)


def search_places(query: str, limit: int) -> list[dict]:
    api_key = os.getenv("GOOGLE_MAPS_API_KEY")
    if not api_key:
        raise RuntimeError("Defina GOOGLE_MAPS_API_KEY no ambiente antes de executar.")

    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": api_key,
        "X-Goog-FieldMask": FIELDS,
    }
    payload = {
        "textQuery": query,
        "maxResultCount": max(1, min(limit, 20)),
        "languageCode": "pt-BR",
        "regionCode": "BR",
    }
    response = requests.post(SEARCH_URL, headers=headers, json=payload, timeout=45)
    response.raise_for_status()
    return response.json().get("places", [])


def normalize(place: dict) -> dict:
    photos = []
    for photo in place.get("photos", [])[:5]:
        photos.append(
            {
                "name": photo.get("name"),
                "widthPx": photo.get("widthPx"),
                "heightPx": photo.get("heightPx"),
                "authorAttributions": photo.get("authorAttributions", []),
            }
        )

    return {
        "place_id": place.get("id"),
        "name": (place.get("displayName") or {}).get("text"),
        "address": place.get("formattedAddress"),
        "primary_type": place.get("primaryType"),
        "rating": place.get("rating"),
        "rating_count": place.get("userRatingCount"),
        "website": place.get("websiteUri"),
        "phone": place.get("nationalPhoneNumber"),
        "google_maps_uri": place.get("googleMapsUri"),
        "photos": photos,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("query", help="Ex.: restaurantes em Santos SP")
    parser.add_argument("--limit", type=int, default=10, help="1 a 20")
    parser.add_argument("--out", default="leads.json")
    args = parser.parse_args()

    try:
        places = search_places(args.query, args.limit)
    except Exception as exc:
        print(f"ERRO: {exc}", file=sys.stderr)
        return 1

    data = {
        "query": args.query,
        "count": len(places),
        "leads": [normalize(p) for p in places],
    }
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Salvo: {out} ({len(places)} leads)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
