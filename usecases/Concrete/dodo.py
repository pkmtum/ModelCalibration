import graphlib
import os
from pathlib import Path
from knowledgeGraph.emodul import validation

baseDir = Path(__file__).resolve().parents[0]
emodulFolder = os.path.join(os.path.join(baseDir,'knowledgeGraph'),'emodul')
emodulRawdataFolder = os.path.join(emodulFolder,'rawdata')
emodulProcesseddataFolder = os.path.join(emodulFolder,'E-modul-processed-data')

compressionFolder = os.path.join(os.path.join(os.path.join(baseDir,'knowledgeGraph'),'compression'),'compression-processed-data')
compressionRawdataFolder = os.path.join(compressionFolder,'rawdata')
compressionProcesseddataFolder = os.path.join(compressionFolder,'processeddata')

graph_path = os.path.join(emodulProcesseddataFolder, 'EM_Graph.ttl')
shapes_path = os.path.join(baseDir, 'shape.ttl')

DOIT_CONFIG = {'verbosity': 2}

def validate_graph(graph_path, shapes_path):
    g = validation.read_graph_from_file(graph_path)
    s = validation.read_graph_from_file(shapes_path)
    r = validation.test_graph(g, s)
    assert validation.violates_shape(r, validation.SCHEMA.InformationBearingEntityShape)
    assert not validation.violates_shape(r, validation.SCHEMA.SpecimenDiameterShape)
    assert not validation.violates_shape(r, validation.SCHEMA.SpecimenShape)

def task_installation():
    yield {
        'basename': 'install python packages',
        'actions': ['pip install -r knowledgeGraph/requirements.txt']
    }

def task_emodul():
    if os.path.exists(os.path.join(os.path.join(os.path.join(baseDir,'knowledgeGraph'),'emodul'),'E-modul-processed-data')):
        yield {
            'basename': 'checking folder',
            'actions': ['echo folder existed']
        }
    else:

        yield {
            'basename': 'create E-modul-processed-data folder',
            'actions': ['mkdir %s ' % emodulFolder]
        }
        yield {
            'basename': 'create rawdata folder',
            'actions': ['mkdir %s ' % emodulRawdataFolder]
        }
        yield {
            'basename': 'create processeddata folder',
            'actions': ['mkdir %s ' % emodulProcesseddataFolder]
        }
    
    yield {
        'basename': 'generate emodul processed data',
        'actions': ['python knowledgeGraph/emodul/emodul_generate_processed_data.py']
    }
    yield {
        'basename': 'extract emodul metadata',
        'actions': ['python knowledgeGraph/emodul/emodul_metadata_extraction.py']
    }
    yield {
        'basename': 'map emodul ontology and metadata',
        'actions': ['python knowledgeGraph/emodul/emodul_mapping.py']
    }
    yield {
        'basename': 'validate rdf files against shacl shape',
        'actions': [(validate_graph, [graph_path, shapes_path])],
        'file_dep': [graph_path]
    }
    yield {
        'basename': 'run emodul query script',
        'actions': ['python knowledgeGraph/emodul/emodul_query.py']
    }
    yield {
        'basename': 'run emodul test query',
        'actions': ['python knowledgeGraph/emodul/emodul_test.py']
    }

def task_compression():
    if os.path.exists(os.path.join(os.path.join(os.path.join(baseDir,'knowledgeGraph'),'compression'),'compression-processed-data')):
        yield {
            'basename': 'checking compression processed data folder',
            'actions': ['echo folder existed']
        }
    else:

        yield {
            'basename': 'create compression-processed-data folder',
            'actions': ['mkdir %s ' % compressionFolder]
        }
        yield {
            'basename': 'create compression rawdata folder',
            'actions': ['mkdir %s ' % compressionRawdataFolder]
        }
        yield {
            'basename': 'create compression processeddata folder',
            'actions': ['mkdir %s ' % compressionProcesseddataFolder]
        }
    yield {
        'basename': 'generate compression processed data',
        'actions': ['python knowledgeGraph/compression/compression_generate_processed_data.py']
    }
    yield {
        'basename': 'extract compression metadata',
        'actions': ['python knowledgeGraph/compression/compression_metadata_extraction.py']
    }
    yield {
        'basename': 'map compression ontology and metadata',
        'actions': ['python knowledgeGraph/compression/compression_mapping.py']
    }
    yield {
        'basename': 'run compression query script',
        'actions': ['python knowledgeGraph/compression/compression_query.py']
    }
    yield {
        'basename': 'run compression test query',
        'actions': ['python knowledgeGraph/compression/compression_test.py']
    }

def task_calibration():
    yield {
        'basename': 'run calibration script',
        'actions': ['python Calibration/E_modul_calibration.py']
    }