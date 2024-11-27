from pinecone_mod.pipeline import Pipeline

def main():
    pipeline=Pipeline(path="../neujsondata",num_dimensions=384)
    pipeline.transform_data()

main()