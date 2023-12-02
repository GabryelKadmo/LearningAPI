from pymongo.mongo_client import MongoClient
from flask import Flask, jsonify, request
from flasgger import Swagger
from bson.objectid import ObjectId

app = Flask(__name__)
swagger = Swagger(app)


uri = "mongodb+srv://kadmo:Gabryel-15@cluster0.p916xyh.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri)
db = client["lista_de_filmes"]
collection_u = db["filmes"]


def serialize_id(document, field_name):
    if field_name in document:
        document[field_name] = str(document[field_name])
    return document


# consultar filmes
@app.route("/filmes", methods=["GET"])
def get_filmes():
    filmes = list(collection_u.find())
    for filme in filmes:
        filme["_id"] = str(filme["_id"])
    # print(filmes)  # Adicione esta linha para visualizar os dados na console
    return jsonify(filmes)


# consultar filmes por id
@app.route("/filmes/<string:_id>", methods=["GET"])
def get_filmes_by_id(_id):
    filme = collection_u.find_one({"_id": ObjectId(_id)})
    if filme:
        filmes = serialize_id(filme, "_id")
        return jsonify(filmes)
    else:
        return jsonify({"error": "Filme não encontrado"}), 404


# Criar
@app.route("/filmes", methods=["POST"])
def create_filmes():
    new_filme = request.get_json()
    filme = collection_u.insert_one(new_filme)
    if filme.acknowledged:
        return jsonify({"id": str(filme.inserted_id)}), 201
    else:
        return jsonify({"error": "Erro ao criar o filme"}), 500


# Editar
@app.route("/filmes/<string:_id>", methods=["PUT"])
def update_filmes_by_id(_id):
    novos_dados_filme = request.get_json()
    filme = collection_u.find_one({"_id": ObjectId(_id)})
    if filme:
        collection_u.update_one({"_id": ObjectId(_id)}, {"$set": novos_dados_filme})
        return jsonify({"message": "Filme atualizado com sucesso"}), 200
    else:
        return jsonify({"error": "Filme não encontrado"}), 404


# excluir
@app.route("/filmes/<string:_id>", methods=["DELETE"])
def delete_filmes_by_id(_id):
  filme = collection_u.find_one({"_id": ObjectId(_id)})
  if filme:
    collection_u.delete_one({"_id": ObjectId(_id)})
    return jsonify({"message": "Filme excluído com sucesso"}), 200
  else:
    return jsonify({"error": "Filme não encontrado"}), 404


if __name__ == "__main__":
    app.run(port=5000, host="learning-api-kadmo", debug=True)