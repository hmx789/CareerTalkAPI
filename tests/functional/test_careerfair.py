from careertalk.models import User, CareerFair, College, CareerFairEmployer, Employer, Degree, HiringType,Visa

from tests.common import _init_test_data_load, test_client, _db, _send_get_for_private_endpoint

print(_init_test_data_load)
print(test_client)
print(_db)


def test_v2_get_companies(test_client, _db):
    # Add a single careerfair and organization
    hogwarts = College(name='hogwarts')
    _db.session.add(hogwarts)
    _db.session.commit()

    magic_careerfair = CareerFair(
        organization_id=str(hogwarts.id),
        name='hogwarts magic career fair',
        date='06/16/2019',
        address='magic and monster street',
        description='too much magic',
        city='hogwarts',
        zipcode='magic',
        other_organization='some other hogwarts',
        map_url='map_url',
        logo_url='logo_url',
        start_time='2:00 PM',
        end_time='3:00 PM',
        location='the great magic hall'
    )

    _db.session.add(magic_careerfair)
    _db.session.commit()
    existing_test_user = User.query.filter_by(first_name='Seho').first()

    existing_careerfair = CareerFair.query\
        .filter_by(name='hogwarts magic career fair')\
        .first()
    CAREERFAIR_EMPLOYERS_ENDPOINT = '/v2/{}/employers'.format(str(magic_careerfair.id))
    print(CAREERFAIR_EMPLOYERS_ENDPOINT)

    # CASE: 0 Participating employers
    user_id = str(existing_test_user.id)
    response = _send_get_for_private_endpoint(
        CAREERFAIR_EMPLOYERS_ENDPOINT,
        test_client,
        user_id
    )
    json_response = response.get_json()

    careerfair_object = {
        'address': 'test_address'
    }
    #{'companies': [],
    # Test some fair components
    assert response.status_code == 200
    assert json_response['companies'] == []
    assert json_response['fair']['address'] == 'magic and monster street'
    assert json_response['fair']['date'] == '06/16/2019'
    assert json_response['fair']['address'] == 'magic and monster street'
    assert json_response['fair']['description'] == 'too much magic'
    assert json_response['fair']['city'] == 'hogwarts'
    assert json_response['fair']['zipcode'] == 'magic'
    assert json_response['fair']['other_organization'] == 'some other hogwarts'
    assert json_response['fair']['map_url'] == 'map_url'
    assert json_response['fair']['logo_url'] == 'logo_url'
    assert json_response['fair']['start_time'] == '2:00 PM'
    assert json_response['fair']['end_time'] == '3:00 PM'
    assert json_response['fair']['location'] == 'the great magic hall'
    assert json_response['num_of_companies'] == 0

    # CASE: 1 Participating employers ( no like, no note)
    google_careerfair_employer = CareerFairEmployer(
        employer_id=str(Employer.query.filter_by(name='Google').first().id),
        careerfair_id=str(magic_careerfair.id),
        degree_type_id=str(Degree.query.filter_by(type='BS, MS, PhD').first().id),
        hiring_type_id=str(HiringType.query.filter_by(type='INT, FT').first().id),
        visa_type_id=str(Visa.query.filter_by(type='yes').first().id)
    )

    _db.session.add(google_careerfair_employer)
    _db.session.commit()

    response = _send_get_for_private_endpoint(
        CAREERFAIR_EMPLOYERS_ENDPOINT,
        test_client,
        user_id
    )
    json_response = response.get_json()

    # Test if the correct companies got returned.
    assert response.status_code == 200
    assert json_response['companies'][0]['employer']['name'] == "Google"
    assert json_response['num_of_companies'] == 1


def test_v2_get_companies_like(test_client, _db):

    pass

def test_v2_get_companies_note(test_client, _db):
    pass
