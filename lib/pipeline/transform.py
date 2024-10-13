import pandas as pd
import requests

def raw_json_to_ds(path: str):
    raw_json_file = pd.read_json(path, encoding='utf-8')
    dataset = pd.DataFrame(raw_json_file)
    return dataset

def filter_ds(dataset: pd.DataFrame):
    filtred_ds = dataset[(dataset['bairro e cep'] != 'Sem informacao') & (dataset['preco'] != 'Sem informacao')].reset_index(drop=True)
    return filtred_ds

def to_float(dataset: pd.DataFrame, columns: list) -> pd.DataFrame:
    result = dataset.copy()
    for column_name in columns:
        result[column_name] = result[column_name].apply(lambda x: _convert_to_float(x))
    return result

def _convert_to_float(value):
    if value == 'Sem informacao':
        return value
    elif '/' in value:
        return float(value.split('/')[0].replace('R$', '').replace('.','').strip())
    else:
        return float(value.replace('R$', '').replace('m²', '').replace('.', '').strip())

def search_cep_viacep(cep):
    response = requests.get(f'https://viacep.com.br/ws/{cep}/json/')
    if response.status_code == 200:
        return response.json()
    else:
        return None

def adress(dataset, column_name):
    intermedian_list_result = []
    for value in dataset[column_name]:
        endereco_dict = {'bairro': 'Sem informação', 'cidade': 'Sem informação', 'estado': 'Sem informação', 'cep': 'Sem informação'}
        splited_column = value.split(',')
        if len(splited_column) < 4:
            endereco = search_cep_viacep(splited_column[-1].strip())
            if 'erro' not in endereco.keys():
                endereco_dict['bairro'] = str(endereco['bairro']).strip()
                endereco_dict['cidade'] = str(endereco['localidade']).strip()
                endereco_dict['estado'] = str(endereco['uf']).strip()
                endereco_dict['cep'] = str(endereco['cep']).strip().replace('-', '')
            else:
                endereco_dict['bairro'] = 'Sem informação'
                endereco_dict['cidade'] = 'Sem informação'
                endereco_dict['estado'] = 'Sem informação'
                endereco_dict['cep'] = 'Sem informação'
        else:
            endereco_dict['bairro'] = splited_column[0].strip()
            endereco_dict['cidade'] = splited_column[1].strip()
            endereco_dict['estado'] = splited_column[2].strip()
            endereco_dict['cep'] = splited_column[3].strip()
        intermedian_list_result.append(endereco_dict)

    result = pd.concat([dataset, pd.DataFrame(intermedian_list_result)], axis=1)
    result = result.drop(column_name, axis=1)
    return result

def dummy_dataset(dataset, columns):
    # Itens para os quais você deseja criar dummies, agora em lower case
    cond_and_imov_itens = ['área de serviço', 'armários no quarto', 'armários na cozinha', 'mobiliado', 'ar condicionado',
                           'churrasqueira', 'varanda', 'academia', 'piscina', 'quarto de serviço', 'condomínio fechado', 'elevador',
                           'permitido animais', 'portaria', 'salão de festas', 'segurança 24h']
    cond_and_imov_itens_set = set(cond_and_imov_itens)

    all_attributes = dataset[columns].apply(lambda x: '\n'.join(x.dropna().unique()).lower(), axis=1)
    
    def create_dummies(row, items):
        dummies = dict.fromkeys(items, 0)
        atributos = row.split('\n')
        for atributo in atributos:
            if atributo in items:
                dummies[atributo] = 1
        dummies_lower = {k.lower(): v for k, v in dummies.items()}
        return pd.Series(dummies_lower)
    
    dummies_df = all_attributes.apply(create_dummies, items=cond_and_imov_itens_set).astype(int)
    
    for col in dummies_df.columns:
        if col in dataset.columns:
            dataset.drop(col, axis=1, inplace=True)
    
    dataset = pd.concat([dataset, dummies_df], axis=1)
    return dataset

def remove_cols(dataset: pd.DataFrame, columns: list):
    return dataset.drop(columns, axis=1)