import database

#testing search for equipment using asset tag
def test_search_equipment(tmp_path,monkeypatch):
    
    # Creating a separate test database for testing
    test_db_path = tmp_path / "test_database.db"
    monkeypatch.setattr(database, "DATABASE", str(test_db_path))
    
    database.create_table()
    
    #adding a chromebook test database
    database.add_equipment("TEST-101","Chromebook","Dell 3100","School 1")
    
    # Search for the Chromebook
    result = database.search_equipment("TEST-101")
    
    #Checking if correct equipment is returned
    assert result is not None
    assert result[0] == "TEST-101"
    assert result[2] == "Dell 3100"
    
    
#Now searching for a asset tag that does not exist in the database
def test_inavlid_asset_tag(tmp_path,monkeypatch):
    
    #Creating a spearte test database
    test_db_path = tmp_path / "test_database.db"
    monkeypatch.setattr(database, "DATABASE", str(test_db_path))
    
    database.create_table()
    
    #Searching for asset tag
    result = database.search_equipment("INVALID-999")
    
    #Checking that wquipment was not found within the database
    assert result is None
    
# Testing search for student using their ID
def test_search_student_id(tmp_path, monkeypatch):

    # Create a separate test database
    test_db_path = tmp_path / "test_database.db"
    monkeypatch.setattr(database, "DATABASE", str(test_db_path))

    database.create_table()

    # Add sample equipment and student IDs
    database.add_demo_equipment()

    # Search using a student ID
    results = database.search_people("STU-002")

    # Check that the correct student and equipment were found
    assert len(results) == 1
    assert results[0][0] == "DEMO-2-001"
    assert results[0][5] == "Sample Student 02"
    assert results[0][7] == "STU-002"
    
    

# Testing search for staff using their name
def test_search_staff_name(tmp_path, monkeypatch):

    # Create a separate test database
    test_db_path = tmp_path / "test_database.db"
    monkeypatch.setattr(database, "DATABASE", str(test_db_path))

    database.create_table()

    # Add sample equipment and staff information
    database.add_demo_equipment()

    # Searching for staff using their name
    results = database.search_people("Sample Staff 07")

    # Checking that the correct staff member and laptop were found
    assert len(results) == 1
    assert results[0][0] == "DEMO-LT-101"
    assert results[0][5] == "Sample Staff 07"
    assert results[0][7] == "STA-007"

# testing search for student or staff that do not exist withint the database
def test_invalid_person(tmp_path, monkeypatch):

    #Creating a speatre test database
    test_db_path = tmp_path / "test_database.db"
    monkeypatch.setattr(database, "DATABASE", str(test_db_path))
    
    database.create_table()
    database.add_demo_equipment()
    
    # Search for ID that is not registered to the database
    results = database.search_people("INVALID-ID")
    
    #Final check no matching record was found
    assert len(results) == 0
