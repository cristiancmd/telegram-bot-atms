class Cajero:
	def __init__(self, id, long, lat, banco, red, ubicacion, localidad, terminales, no_vidente, dolares, calle, altura, calle2, barrio, comuna, codigo_postal, codigo_postal_argentino, extracciones):
		self.id = id
		self.long = long
		self.lat = lat
		self.banco = banco
		self.red = red
		self.ubicacion = ubicacion
		self.localidad = localidad
		self.terminales = terminales
		self.no_vidente = no_vidente
		self.dolares = dolares
		self.calle = calle
		self.altura = altura
		self.calle2 = calle2
		self.barrio = barrio
		self.comuna = comuna
		self.codigo_postal = codigo_postal
		self.codigo_postal_argentino = codigo_postal_argentino
		self.extracciones = extracciones


	def get_id(self):
		return self.id

	def get_long(self):
		return self.long

	def get_lat(self):
		return self.lat

	def get_banco(self):
		return self.banco

	def get_red(self):
		return self.red

	def get_ubicacion(self):
		return self.ubicacion

	def get_localidad(self):
		return self.localidad

	def get_terminales(self):
		return self.terminales

	def get_no_vidente(self):
		return self.no_vidente

	def get_dolares(self):
		return self.dolares

	def get_calle(self):
		return self.calle

	def get_altura(self):
		return self.altura

	def get_calle2(self):
		return self.calle2

	def get_barrio(self):
		return self.barrio

	def get_comuna(self):
		return self.comuna

	def get_codigo_postal(self):
		return self.codigo_postal

	def get_codigo_postal_argentino(self):
		return self.codigo_postal_argentino


	def __str__():
 		return "id: " + id + " , " + "long: " + long + " , " + "lat: " + lat + " , " + "banco: " + banco + " , " + "red: " + red + " , " + "ubicacion: " + ubicacion + " , " + "localidad: " + localidad + " , " + "terminales: " + terminales + " , " + "no_vidente: " + no_vidente + " , " + "dolares: " + dolares + " , " + "calle: " + calle + " , " + "altura: " + altura + " , " + "calle2: " + calle2 + " , " + "barrio: " + barrio + " , " + "comuna: " + comuna + " , " + "codigo_postal: " + codigo_postal + " , " + "codigo_postal_argentino: " + codigo_postal_argentino
