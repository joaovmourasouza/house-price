
from lib.pipeline import process, search, transform
from lib.operations import save, load

if __name__ == "__main__":
    # Extração de links
    links_extracted = search.links()
    saved_links_path = save.json_file(path='links', name='links', data=links_extracted)

    # Extração das informações dos imóveis
    links_extracted_loaded = load.json_file(path=saved_links_path)
    raw_data = process.links(links=links_extracted_loaded)
    raw_data_path = save.json_file(path='data/bronze', name='raw_data', data=raw_data)

    # Transformação dos dados
    dataset = transform.raw_json_to_ds(path=raw_data_path)
    dataset = transform.filter_ds(dataset=dataset)
    dataset = transform.to_float(dataset=dataset, columns=['preco', 'area util por m²', 'custo condominio', 'iptu'])
    dataset = transform.adress(dataset=dataset, column_name='bairro e cep')
    dataset = transform.dummy_dataset(dataset=dataset, columns=['caracteristica do imovel', 'caracteristica do condominio'])
    dataset = transform.remove_cols(dataset=dataset, columns=['caracteristica do imovel', 'caracteristica do condominio'])
    
    # Carregamentos dos dados
    csv_data_path = save.csv_file(path='data/silver', name='silver_dataset', dataset=dataset)
    merging_datasets = save.merge_datasets()