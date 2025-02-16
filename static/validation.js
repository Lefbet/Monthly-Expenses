function validate_index() {
    /* Validate index entries */
    let error = "";

    let year = document.querySelector('#year').value;
    if (year == "Select Year") {
        error = "year is required";
        document.querySelector('#error_msg').innerHTML = error;
        return false;
    }

    let month = document.querySelector('#month').value;
    if (month == "Select Month") {
        error = "month is required";
        document.querySelector('#error_msg').innerHTML = error;
        return false;
    }

    return true;
} // validate_index()


function validate_login() {
    /* Validate login entries */
    let error = "";

    let un = document.querySelector('#username').value;
    if (un == "") {
        error = "username is required";
        document.querySelector('#error_msg').innerHTML = error;
        return false;
    }
    if (un.length < 3) {
        error = "username must be at least 3 characters long";
        document.querySelector('#error_msg').innerHTML = error;
        return false;
    }

    let pw = document.querySelector('#password').value;
    if (pw == "") {
        error = "password is required";
        document.querySelector('#error_msg').innerHTML = error;
        return false;
    }
    if (pw.length < 4) {
        error = "password must be at least 4 characters long";
        document.querySelector('#error_msg').innerHTML = error;
        return false;
    }

    return true;
} // validate_login()


function validate_register() {
    /* Validate register entries */
    let error = "";

    let un = document.querySelector('#username').value;
    if (un == "") {
        error = "username is required";
        document.querySelector('#error_msg').innerHTML = error;
        return false;
    }
    if (un.length < 3) {
        error = "username must be at least 3 characters long";
        document.querySelector('#error_msg').innerHTML = error;
        return false;
    }

    let pw = document.querySelector('#password').value;
    if (pw == "") {
        error = "password is required";
        document.querySelector('#error_msg').innerHTML = error;
        return false;
    }
    if (pw.length < 4) {
        error = "password must be at least 4 characters long";
        document.querySelector('#error_msg').innerHTML = error;
        return false;
    }

    let confirm = document.querySelector('#confirmation').value;
    if (confirm == "") {
        error = "password confirmation is required";
        document.querySelector('#error_msg').innerHTML = error;
        return false;
    }
    if (!(confirm === pw)) {
        error = "passwords do not match";
        document.querySelector('#error_msg').innerHTML = error;
        return false;
    }

    return true;
} // validate_register()


function validate_change_password() {
    /* Validate password change entries */
    let error = "";

    let oldpw = document.querySelector('#oldpassword').value;
    if (oldpw == "") {
        error = "old password is required";
        document.querySelector('#error_msg').innerHTML = error;
        return false;
    }
    if (oldpw.length < 4) {
        error = "password must be at least 4 characters long";
        document.querySelector('#error_msg').innerHTML = error;
        return false;
    }

    let newpw = document.querySelector('#newpassword').value;
    if (newpw == "") {
        error = "new password is required";
        document.querySelector('#error_msg').innerHTML = error;
        return false;
    }
    if (newpw.length < 4) {
        error = "password must be at least 4 characters long";
        document.querySelector('#error_msg').innerHTML = error;
        return false;
    }

    let confirm = document.querySelector('#confirmation').value;
    if (confirm == "") {
        error = "password confirmation is required";
        document.querySelector('#error_msg').innerHTML = error;
        return false;
    }
    if (!(confirm === newpw)) {
        error = "passwords do not match";
        document.querySelector('#error_msg').innerHTML = error;
        return false;
    }

    if (newpw === oldpw) {
        error = "new password can not be the same as the old one";
        document.querySelector('#error_msg').innerHTML = error;
        return false;
    }

    return true;
} // validate_change_password()


function validate_add() {
    /* Validate add expense entries */
    let error = "";

    let category = document.querySelector('#category').value;
    if (category == "Category") {
        error = "category is required";
        document.querySelector('#error_msg').innerHTML = error;
        return false;
    }

    let amount = Number(document.querySelector('#amount').value);
    if (isNaN(amount)) {
        error = "amount must be a positive number";
        document.querySelector('#error_msg').innerHTML = error;
        return false;
    } else {
        if (amount <= 0) {
            error = "amount must be a positive number";
            document.querySelector('#error_msg').innerHTML = error;
            return false;
        }
    }

    return true;
} // validate_add()


function validate_categories() {
    /* Validate categories entries */
    let error = "";

    let newcategory = document.querySelector('#newcategory').value;
    if (newcategory == "") {
        error = "category is required";
        document.querySelector('#error_msg').innerHTML = error;
        return false;
    }

    return true;
} // validate_categories()


function confirmation() {
    return confirm("Are you sure you want to remove this expense?");
} // confirmation()

