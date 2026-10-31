
import boto3

# Región donde creamos nuestra tabla de DynamoDB
AWS_REGION = "us-east-1"

# Conexión con el servicio DynamoDB
dynamodb = boto3.resource(
    "dynamodb",
    region_name=AWS_REGION,
)

# Referencia a nuestra tabla
urls_table = dynamodb.Table("url-shortener")


def check_database_connection():
    """
    Comprueba que podemos comunicarnos con DynamoDB.
    """
    urls_table.load()
    return True
