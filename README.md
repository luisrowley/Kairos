# Kairos
Kairos is a vulnerability assesment tool for the web based on [side-channel timing attacks](https://en.wikipedia.org/wiki/Side-channel_attack). This tool allows the researcher to find valid **user names** on a target web URL, given that the website login is flawed by design. 

## Usage
```bash
python3 kairos.py [-h] [-w WORDLIST] [-u URL] [-n ROUNDS] [-X HTTP_METHOD]
```

## How does it work?
This assessment tool relies on a structural flaw on the design of a login system in which the existence of a user is checked beforehand. In a vulnerable web, once a first call to check if a user exists is made to the backend, only then the system checks if the password matches and hashes the plain-text password submited by the user:

```php
<?php

// get user from DB based in POST param
$user = $db->query('SELECT * FROM users WHERE username="'.$_POST['userid'].'"');

// check user exists
if ($user) {
    ...
  // calculate password hash from POST
  $pass = hash_password($_POST['passwd']);
  // get user data
  $db_password = mysqli_fetch_row($user)['db_password'];
  
  // check if received password matches with one stored in the database
  if ($pass === $db_password) {
      // user login is valid
	...
  } else {
    // error: wrong password
    ...
  }
} else {
// error: user doesn't exist
...
}  
```

Therefore the **extra time** it takes for the backend system to compute the password hash allows us to determine if a user exists or not in the system independently of any log messages.

## Requirements
[Python](https://www.python.org/downloads/) version > 3.6 or more

## See it in action

### Launch sample Request

### Understanding the results

## Disclaimer

For educational purposes only. The author(s) is not responsible for any misuse or damage caused by this tool to any user(s) or third parties.