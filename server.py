class Server:
    def __init__(self, nome_istanza, stato_istanza, regione_istanza, region_electricity_map, carbon_intensity, id_istanza):
        self.nome_istanza = nome_istanza
        self.stato_istanza = stato_istanza
        self.regione_istanza = regione_istanza
        self.region_electricity_map = region_electricity_map
        self.carbon_intensity = carbon_intensity
        self.id_istanza = id_istanza

    def get_nome_istanza(self):
        return self.nome_istanza

    def set_nome_istanza(self, nome_istanza):
        self.nome_istanza = nome_istanza

    def get_stato_istanza(self):
        return self.stato_istanza

    def set_stato_istanza(self, stato_istanza):
        self.stato_istanza = stato_istanza

    def get_regione_istanza(self):
        return self.regione_istanza

    def set_regione_istanza(self, regione_istanza):
        self.regione_istanza = regione_istanza

    def get_region_electricity_map(self):
        return self.region_electricity_map

    def set_region_electricity_map(self, region_electricity_map):
        self.region_electricity_map = region_electricity_map

    def get_carbon_intensity(self):
        return self.carbon_intensity

    def set_carbon_intensity(self, carbon_intensity):
        self.carbon_intensity = carbon_intensity

    def get_id_istanza(self):
        return self.id_istanza

    def __str__(self):
        return f"Server [id_istanza={self.id_istanza}, nome_istanza={self.nome_istanza}, stato_istanza={self.stato_istanza}, regione_istanza={self.regione_istanza}, region_electricity_map={self.region_electricity_map}, carbon_intensity={self.carbon_intensity}]"
