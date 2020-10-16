#! /usr/bin/python3

#
# This file is part of Callisto software
# Callisto helps scientists to share data between collaborators
# 
# Callisto is free software: you can redistribute it and/or modify
# it under the terms of the GNU AFFERO GENERAL PUBLIC LICENSE as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
#  Copyright (C) 2019-2021    C A L M I P
#  callisto is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU AFFERO GENERAL PUBLIC LICENSE for more details.
#
#  You should have received a copy of the GNU AFFERO GENERAL PUBLIC LICENSE
#  along with Callisto.  If not, see <http://www.gnu.org/licenses/agpl-3.0.txt>.
#
#  Authors:
#        Thierry Louge      - C.N.R.S. - UMS 3667 - CALMIP
#        Emmanuel Courcelle - C.N.R.S. - UMS 3667 - CALMIP
#

import os
import json
import time
from rdflib import Graph, URIRef, Literal
from rdflib import Namespace
from rdflib.namespace import OWL, RDF, RDFS
import logging as log
from franz.openrdf.sail.allegrographserver import AllegroGraphServer
from franz.openrdf.repository.repository import Repository
from franz.openrdf.vocabulary import RDF
from franz.openrdf.query.query import QueryLanguage

class DatasetsToOntology(object):
    """
    """
    def get_details(self):
        """
        Récupère et analyse le json du contenu des dataverses.
        Pour bien voir la structure d'un fichier, chaine ou url
        contenant du json: https://jsoneditoronline.org/
        :return:
        liste de listes de 4 éléments comprenant: id, titre, description, et liste de sujets liés au dataset
        prototype de chaque liste: [string, string, string, [string,...,string]]
        """
        API_TOKEN = "e0967c6e-4679-4c4b-b74f-4e165bd6866c"
        SERVER_URL = "Callistodataverse:8080"
        stores = ["demonstration"]
        liste_results = []

        for store in stores:
            os.system(
                "wget " + SERVER_URL + "/api/dataverses/" + store + "/contents?key=" + API_TOKEN + " --no-check-certificate -O contenu.json")
            with open('contenu.json', 'r') as f:
                data_dict = json.load(f)
            # print(data_dict["data"])
            # print(type(data_dict["data"]))
            for data in data_dict["data"]:
                # print(data)
                # print(type(data))
                # print(data['id'])
                keywords = []
                #print(SERVER_URL + "/api/datasets/" + str(data['id']) + "?key=" + API_TOKEN)
                os.system("wget " + SERVER_URL + "/api/datasets/" + str(
                    data['id']) + "?key=" + API_TOKEN + " --no-check-certificate -O data.json")
                #print(SERVER_URL + "/api/datasets/" + str(data['id']) + "?key=" + API_TOKEN + " --no-check-certificate -O data.json")
                with open('data.json', 'r') as datasets:
                    liste_datasets = json.load(datasets)
                    # print(type(liste_datasets['data']))
                    # print(type(liste_datasets['data']['latestVersion']['files']))
                    # print(liste_datasets['data']['latestVersion']['files'])
                    for elt in liste_datasets['data']['latestVersion']['files']:

                        # print(elt)
                        # On récupère l'id des datasets du dataverse interrogé
                        if isinstance(elt, dict):
                            id_elt = elt['dataFile']['id']
                            #print("id datafile:" + str(id_elt))
                            type_elt = elt['dataFile']['contentType']
                            #print("type datafile:" + str(type_elt))
                            url = SERVER_URL + "/api/access/datafile/" + str(id_elt) + "?key=" + API_TOKEN
                    for elt in liste_datasets['data']['latestVersion']['metadataBlocks']['citation']['fields']:
                        # print(str(type(elt)) + "-->" + str(elt))
                        if elt["typeName"] == "title":
                            # Recupere le titre du dataset
                            resume = elt["value"]
                            #print("resume:" + str(resume))
                        if elt["typeName"] == "dsDescription":
                            # Recupere la description du dataset
                            for description_index in elt['value']:
                                description = description_index['dsDescriptionValue']['value']
                                print("description:" + str(description))
                        if elt["typeName"] == "subject":
                            # Recupere les mots-clés des vocabulaires controlés liés au dataset
                            subjects = elt["value"]
                            #print(type(subjects))
                            #print("subject:" + str(subjects))
                            keywords.append(subjects)
                        if elt["typeName"] == "keyword":
                            # Recupere les mots-clés des vocabulaires controlés liés au dataset
                            for path in elt["value"]:
                                #print("keyword:" + str(path["keywordValue"]["value"]))
                                keywords.append(path["keywordValue"]["value"])
                    #for elt in liste_datasets['data']['latestVersion']['files']:
                        #print(str(elt))
                        #print(elt["typeName"])
                        #if elt["typeName"] == "contentType":
                            # Recupere les mots-clés des vocabulaires controlés liés au dataset
                            #print ("type" + str(elt["value"]))
                    liste_results.append([id_elt, resume, description, subjects, url, keywords, type_elt])
        return liste_results

    def get_registered_datasets(self):
        """
        Get registered datasets on the repository so that 
        datasets won't be registered multiple times
        """
        self.registered_descriptions = []
        queryString = """PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX oboInOwl: <http://www.geneontology.org/formats/oboInOwl#>
        PREFIX edamontology: <http://edamontology.org/>
        PREFIX obo: <http://purl.obolibrary.org/obo/>
        PREFIX arcas: <http://www.callisto.calmip.univ-toulouse.fr/ARCAS.rdf#>
        PREFIX service: <http://www.daml.org/services/owl-s/1.2/Service.owl#>
        PREFIX profile: <http://www.daml.org/services/owl-s/1.2/Profile.owl#>
        PREFIX mp:<http://purl.org/mp#>
        SELECT DISTINCT ?description
        WHERE {
        ?service service:presents ?profile.
        ?profile arcas:hasQuerySoftware "http://www.callisto.calmip.univ-toulouse.fr/ARCAS.rdf#get_dataset".
        ?profile profile:textDescription ?description.
        }"""
        tupleQuery = self.conn.prepareTupleQuery(QueryLanguage.SPARQL, queryString)
        log.info(queryString)
        result = tupleQuery.evaluate()
        with result:
            for binding_set in result:
                #print("Allegro description:")
                #print(str(binding_set.getValue("description")).encode('utf8'))
                self.registered_descriptions.append(str(binding_set.getValue("description")).replace("\"","").replace("\\n","").replace("\\r"," ").replace("\\","").encode('utf8'))
        #for elt in self.registered_descriptions:
            #print(elt)
                	
    def update_ontology(self, details):
        """
        Met a jour l'ontologie avec les éléments recueillis dans get_details
        :return:
        Ontologie mise a jour
        """
        #print ("details: " + str(details))
        service = Namespace("http://www.daml.org/services/owl-s/1.2/Service.owl#")
        profile = Namespace("http://www.daml.org/services/owl-s/1.2/Profile.owl#")
        mp = Namespace("http://purl.org/mp/")
        mp2 = Namespace("http://purl.org/mp#")
        provo = Namespace("http://www.w3.org/ns/prov#")
        dc = Namespace("http://purl.org/dc/terms#")
        arcas = Namespace("http://www.callisto.calmip.univ-toulouse.fr/ARCAS.rdf#")
        myont = Namespace("http://callisto-local.mydomain.callisto.th/DEMONSTRATION.rdf#")
        print('Repository contains %d statement(s).' % self.conn.size())
        self.get_registered_datasets()
        # Add the OWL data to the graph
        for elt in details:
            timer = str(time.time())
            svc = timer + "_" + str(elt[0])
            profile_id = svc + "_Profile"
            short_url = timer + "_url"
            aggregate = timer + "_agg"

            measurement = "Quantity that is measured"
            keywords = elt[5]
            elt_type =  elt[6]
            resume = str(elt[1])
            description = str(elt[2])
            subjects = str(elt[3])
            url = str(elt[4])
            unit = "UNITLESS"

            #print("svc: "+svc)
            #print("URL is: --> "+url)
            #print("keywords:" + str(keywords))
            same = 0
            for reg_desc in self.registered_descriptions:
                print("description:" + description)
                print("comparing with:")
                print(reg_desc)
                if description in str(reg_desc):
                    same = 1
                    break
            if same == 1:
                continue
            #print("measurement:" + measurement)
            #print("resume:" + resume)
            #print("subjects:" + subjects)
            #print(URIRef(service.Service))

            qualifies = self.conn.createURI(URIRef(mp2.qualifies))
            presents = self.conn.createURI(URIRef(service.presents))
            hasoperation = self.conn.createURI(URIRef(arcas.hasOperation))
            hasQuerySoftware = self.conn.createURI(URIRef(arcas.hasQuerySoftware))
            hasOutput = self.conn.createURI(URIRef(arcas.hasOutput))
            hasInput =  self.conn.createURI(URIRef(arcas.hasInput))
            isCombinedToParam =  self.conn.createURI(URIRef(arcas.isCombinedToParam))
            isCombinedToFormat =  self.conn.createURI(URIRef(arcas.isCombinedToFormat))
            isCombinedToUnit =  self.conn.createURI(URIRef(arcas.isCombinedToUnit))
            ApiKey = self.conn.createURI(URIRef(myont.ApiKey))

            labels = self.conn.createURI("<http://www.w3.org/2000/01/rdf-schema#label>")
            isDefined = self.conn.createURI("<http://www.w3.org/2000/01/rdf-schema#isDefinedBy>")
            servi = self.conn.createURI("<http://www.callisto.calmip.univ-toulouse.fr/SMS.rdf#"+ svc+">")
            profile = self.conn.createURI("<http://www.callisto.calmip.univ-toulouse.fr/SMS.rdf#" + profile_id+">")
            data_tim = self.conn.createURI("<http://www.callisto.calmip.univ-toulouse.fr/SMS.rdf#" + timer+">")
            data_url = self.conn.createURI("<http://www.callisto.calmip.univ-toulouse.fr/SMS.rdf#" + url+">")
            agg = self.conn.createURI("<http://www.callisto.calmip.univ-toulouse.fr/SMS.rdf#" + aggregate+">")
            self.conn.add(servi, RDF.TYPE, URIRef(service.Service))
            self.conn.add(profile, RDF.TYPE, URIRef(service.ServiceProfile))
            self.conn.add(data_tim,RDF.TYPE, URIRef(arcas.MeasuredQuantity))

            self.conn.add(servi, presents, profile)
            
            self.conn.add(servi, hasoperation,  URIRef(arcas.retrieve_dataset))
            self.conn.add(servi, hasoperation, URIRef(arcas.retrieve_metadata))
            self.conn.add(profile, hasQuerySoftware, URIRef(arcas.get_dataset))
            self.conn.add(profile,"<http://www.daml.org/services/owl-s/1.2/Profile.owl#textDescription>", Literal(description))
            self.conn.add(agg, RDF.TYPE, URIRef(arcas.Aggregate))

            self.conn.add(servi, hasOutput, agg)
            self.conn.add(servi, hasInput, ApiKey)
            #self.conn.add(agg,"<http://callisto.calmip.univ-toulouse.fr/callisto/ARCAS.rdf#isCombinedToParam>",Literal(measurement))
            # Quantity
            
            self.conn.add(servi,"<http://www.w3.org/2000/01/rdf-schema#isDefinedBy>", Literal(measurement))
            for word in range(len(keywords)):
                #print (keywords[word])
                if isinstance(keywords[word],str):
                    clean_word = keywords[word].rstrip("']").lstrip("['").replace("'","").replace(",","")
                    #ref = "<http://callisto.calmip.univ-toulouse.fr/callisto/ARCAS.rdf#" + clean_word.replace(" ", "") +">"
                    #print("Referencing KEYWORD: " + ref)
                    #uri_ref = self.conn.createURI(ref)
                    #self.conn.add(uri_ref, RDF.TYPE, URIRef(mp.SemanticQualifier))
                    #self.conn.add(uri_ref, "<http://www.w3.org/2000/01/rdf-schema#label>", Literal(clean_word))
                    #self.conn.add(uri_ref, "<http://www.w3.org/2000/01/rdf-schema#isDefinedBy>", Literal(clean_word))
                    quantity = self.conn.createURI("<http://www.callisto.calmip.univ-toulouse.fr/SMS.rdf#" + clean_word.replace(" ", "")+">")
                    label = self.conn.createURI("<http://www.callisto.calmip.univ-toulouse.fr/SMS.rdf#" + clean_word+">")
                    #print("quantity created")
                    #print(agg)
                    #print(isCombinedToParam)
                    #print(quantity)
                    self.conn.add(agg,isCombinedToParam,quantity)
                    self.conn.add(quantity,isDefined,label)
                    #self.conn.add(quantity,labels,label)
                else:
                    for stage2 in range(len(keywords[word])):
                        clean_word = keywords[word][stage2].rstrip("']").lstrip("['").replace("'","").replace(",","")
                        label = self.conn.createURI("<http://www.callisto.calmip.univ-toulouse.fr/SMS.rdf#" + clean_word+">")
                        quantity = self.conn.createURI("<http://www.callisto.calmip.univ-toulouse.fr/SMS.rdf#" + clean_word.replace(" ", "")+">")
                        #print("quantity created")
                        #print(agg)
                        #print(isCombinedToParam)
                        #print(quantity)
                        self.conn.add(agg,isCombinedToParam,quantity)
                        self.conn.add(quantity,isDefined,label)
                        self.conn.add(quantity,labels,label)
                        #ref = "<http://callisto.calmip.univ-toulouse.fr/callisto/ARCAS.rdf#" + clean_word.replace(" ", "") +">"
                        #print("Referencing KEYWORD on stage2:" + ref)
                        #uri_ref = self.conn.createURI(ref)
                        #self.conn.add(uri_ref, RDF.TYPE, URIRef(mp.SemanticQualifier))
                        #self.conn.add(uri_ref, "<http://www.w3.org/2000/01/rdf-schema#label>", Literal(clean_word))
                        #self.conn.add(uri_ref, "<http://www.w3.org/2000/01/rdf-schema#isDefinedBy>", Literal(clean_word))
                        #self.conn.add(agg,isCombinedToParam,uri_ref)
                        #self.conn.add(uri_ref,qualifies, servi)
                        

            self.conn.add(data_tim, RDF.TYPE, URIRef(mp.Data))
            # self.conn.add((URIRef("http://callisto.calmip.univ-toulouse.fr/callisto/ARCAS.rdf#"+creator_id),\
            #             URIRef(dc.creator),\
            #             URIRef("http://callisto.calmip.univ-toulouse.fr/callisto/ARCAS.rdf#"+timer)))
            # self.conn.add((URIRef("http://callisto.calmip.univ-toulouse.fr/callisto/ARCAS.rdf#"+timer),\
            #             URIRef(mp.authoredBy),\
            #             URIRef("http://callisto.calmip.univ-toulouse.fr/callisto/ARCAS.rdf#"+author_id)))
            self.conn.add(data_tim,"<http://www.w3.org/2000/01/rdf-schema#isDefinedBy>",Literal(description))

            # Format
            # Reify this with formats from swo is needed. http://edamontology.org/format_1915
            uri_format = self.conn.createURI("http://callisto.calmip.univ-toulouse.fr/callisto/SMS.rdf#" + elt_type)
            #uri_unit = self.conn.createURI("http://callisto.calmip.univ-toulouse.fr/callisto/ARCAS.rdf#" + self.unit)
            self.conn.add(uri_format, RDF.TYPE, URIRef(arcas.Format))
            #self.conn.add(uri_unit, RDF.TYPE, URIRef(arcas.Unit))
            
            # # Unit:
            
            # self.conn.add((URIRef("http://callisto.calmip.univ-toulouse.fr/callisto/ARCAS.rdf#" + \
            #                     agg), URIRef(arcas.isCombinedToParam), \
            #              URIRef("http://callisto.calmip.univ-toulouse.fr/callisto/ARCAS.rdf#" + timer)))
            self.conn.add(agg, isCombinedToFormat, uri_format)
            self.conn.add(agg, isCombinedToUnit, URIRef(arcas.unitless))
            # # Outputs:
            #

            self.conn.add(servi,"<http://www.callisto.calmip.univ-toulouse.fr/ARCAS.rdf#hasOutput>",agg)

            # AccessURL:
            self.conn.add(data_url, RDF.TYPE, URIRef(arcas.accessURL))
            self.conn.add(data_url, "<http://www.w3.org/2000/01/rdf-schema#isDefinedBy>", Literal(url))
            self.conn.add(servi,"<http://www.callisto.calmip.univ-toulouse.fr/ARCAS.rdf#isAccessedThrough>",data_url)
            print('Repository contains %d statement(s).' % self.conn.size())

    def open_connection(self,repo):
        server=AllegroGraphServer(host=self.host,port=self.port,user=self.user,password=self.password)
        catalog = server.openCatalog('')
        mode = Repository.OPEN
        repository = catalog.getRepository(repo, mode)
        conn = repository.getConnection()
        return [repository,conn]

    def close_connection(self):
        self.conn.close()
        self.repo.shutDown()

    def __init__(self):
        os.system("rm allegro_fcts.log")
        log.basicConfig(filename='Datasets_to_allegro.log', level=log.DEBUG, format='%(levelname)s:%(asctime)s %(message)s ')
        self.host = "CallistoAllegro"
        self.port = {{allegro_port}}
        self.user = "{{allegro_user}}"
        self.password = "{{allegro_password}}"
        repo = "demonstration"
        self.repo = self.open_connection(repo)[0]
        self.conn = self.open_connection(repo)[1]

