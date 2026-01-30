Feature: School Manager API

  Scenario: User is able to register 2 users
    Given School system is empty
    When I register a user with email: "kurt@cobain.com", age: "27", region: "US"
    And I register a user with email: "tadeusz@szczesniak.pl", age: "30", region: "PL"
    Then Number of users in system equals: "2"
    And User with email "kurt@cobain.com" exists in system
    And User with email "tadeusz@szczesniak.pl" exists in system

  Scenario: User is able to update course price
    Given School system is empty
    And I create a course titled: "Python Basics" with price: "100", materials: "5", owner: "Marek"
    When I update "price" of course "Python Basics" to "150"
    Then Course "Python Basics" has "price" equal to "150"

  Scenario: User is able to update course title
    Given School system is empty
    And I create a course titled: "Java" with price: "200", materials: "10", owner: "Ania"
    When I update "title" of course "Java" to "Java Master"
    Then Course "Java Master" exists in system
    And Course "Java" does not exist in system

  Scenario: User is able to delete a course
    Given School system is empty
    And I create a course titled: "C++" with price: "50", materials: "2", owner: "Boss"
    When I delete course with title: "C++"
    Then Course "C++" does not exist in system
    And Number of courses in system equals: "0"

  Scenario: Full enrollment and review flow
    Given School system is empty
    And I register a user with email: "student@test.pl", age: "20", region: "PL"
    And I create a course titled: "Testing" with price: "80", materials: "3", owner: "Admin"
    And Course "Testing" is published
    When I enroll user "student@test.pl" to course "Testing"
    And I add review for course "Testing" from "student@test.pl" with rating: "5" and comment: "Great!"
    Then Course "Testing" has "1" reviews