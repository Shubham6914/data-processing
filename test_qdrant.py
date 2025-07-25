from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

def test_qdrant_connection():
    try:
        # Connect to Qdrant
        client = QdrantClient("localhost", port=6333)
        print("✅ Successfully connected to Qdrant")
        
        # Create a test collection
        client.create_collection(
            collection_name="test_collection",
            vectors_config=VectorParams(size=4, distance=Distance.COSINE)
        )
        print("✅ Successfully created test collection")
        
        # Insert a test point
        test_vector = [0.1, 0.2, 0.3, 0.4]
        client.upsert(
            collection_name="test_collection",
            points=[
                PointStruct(
                    id=1,
                    vector=test_vector,
                    payload={"test": "data"}
                )
            ]
        )
        print("✅ Successfully inserted test data")
        
        # Search test
        search_result = client.search(
            collection_name="test_collection",
            query_vector=test_vector,
            limit=1
        )
        print("✅ Successfully performed search operation")
        
        # Cleanup
        client.delete_collection(collection_name="test_collection")
        print("✅ Successfully cleaned up test collection")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    print("Starting Qdrant Test...")
    success = test_qdrant_connection()
    if success:
        print("\n🎉 All tests passed! Qdrant is working correctly!")
    else:
        print("\n❌ Some tests failed. Please check the errors above.")