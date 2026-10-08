Feature: Booking a seat

  Scenario: A logged-in user books an available seat
    Given a movie "Inception" exists
    And a seat "A1" is available
    And I am logged in as "alice"
    When I book seat "A1" for "Inception"
    Then seat "A1" is marked as booked
    And "alice" has 1 booking

  Scenario: A booked seat cannot be booked again
    Given a movie "Inception" exists
    And a seat "A2" is already booked
    And I am logged in as "alice"
    When I book seat "A2" for "Inception"
    Then the booking is rejected
    And "alice" has 0 bookings