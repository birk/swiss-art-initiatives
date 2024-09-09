# Self-organized Art Initiatives in Switzerland

This data set was created as part of the ["Off OffOff Of?"](https://www.hslu.ch/en/lucerne-university-of-applied-sciences-and-arts/research/projects/detail/?pid=1045) research project at the Lucerne School of Design, Film and Art. It contains information about more than 700 self-organized art initiatives in Switzerland and is the basis for the project website [selbstorganisation-in-der-kunst.ch](https://selbstorganisation-in-der-kunst.ch).

The data set consist of 3 tables, where `data/projects.csv` is the main table and `data/people.csv` and `data/places.csv` refer to it with additional information. `datapackage.json` explains the structure and the data types according to [Frictionless Data](https://frictionlessdata.io) conventions.

The data set requires further cleaning, which is planned for [GLAMhack24](https://opendata.ch/de/events/glamhack24/).

[![Frictionless](https://github.com/birk/swiss-art-initiatives/actions/workflows/frictionless.yaml/badge.svg)](https://repository.frictionlessdata.io/pages/dashboard.html?user=birk&repo=swiss-art-initiatives&flow=frictionless)

## Processing steps

- Geocoordinates (WGS84) have been added to `data/places.csv` via `retrieve_WGS84.py` using the Nominatim API.
- Data has been cleaned and adapted for Wikidata using [OpenRefine](https://openrefine.org).
- Reconciled against Wikidata, Q-numbers have been added to the data sets.

## Wikidata

Parts of the data have been ingested to Wikidata. The ingested self-organized art initiatives are identified as [described by source (P1343)](http://www.wikidata.org/entity/P1343) [Unabhängig, prekär, professionell (Q130250557)](http://www.wikidata.org/entity/Q130250557), the main publication of the research project.

The following queries can be used to retrieve the data.

Simple list of all initiatives:

```SPARQL
SELECT ?item ?itemLabel WHERE
{
  ?item wdt:P1343 wd:Q130250557.
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
}
```

[https://w.wiki/B99B](https://w.wiki/B99B)

Example of a list with additional information:

```SPARQL
SELECT ?item ?itemLabel ?placeLabel ?start ?end WHERE
{
  ?item wdt:P1343 wd:Q130250557.
  OPTIONAL {
    ?item wdt:P276 ?place.
  }
  OPTIONAL {
    ?item wdt:P571 ?start.
  }
  OPTIONAL {
    ?item wdt:P576 ?end.
  }
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
}
```

[https://w.wiki/B99K](https://w.wiki/B99K)

World map of self-organized art initiatives:

```SPARQL
#defaultView:Map
SELECT DISTINCT ?project ?projectLabel ?geo WHERE {
  { ?project wdt:P31 wd:Q3325736. }
  UNION
  { ?project wdt:P31 wd:Q4034417. }
  # ?project wdt:P17 wd:Q39. # Switzerland only
  ?project wdt:P625 ?geo.
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
}
```

[https://w.wiki/B99N](https://w.wiki/B99N)

## License

The content of the research project "Off OffOff Of?" is released under the license [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), unless differently stated; the structured data about the self-organized art initiatives are released with the license [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/).
