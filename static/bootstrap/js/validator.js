/**
 * Created by zhonzhen on 4/16/16.
 */
function emailValidtor() {
    var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    var address = document.getElementById("emailAddr").value;
    var form = document.getElementById("formDiv");
    var sign = document.getElementById("sign");

    if(re.test(address)) {
        form.className = "form-group has-success has-feedback input-group-lg";
        sign.className = "glyphicon glyphicon-ok form-control-feedback";
        return true;
    }
    else{
        form.className = "form-group has-error has-feedback input-group-lg";
        sign.className = "glyphicon glyphicon-remove form-control-feedback";
        return false;
    }
}


function subSubmitCheck() {
    var form = document.getElementById("formDiv");
    var sign = document.getElementById("sign");
    var checkBoxes = document.getElementsByName("sources");
    var checkBoxValid = false;

    if (emailValidtor()) {
        for (var i = 0; i < checkBoxes.length; i++) {
            if (checkBoxes[i].checked) {
                checkBoxValid = true;
                break;
            }
        }
        if (!checkBoxValid) {
            document.getElementById("checkBoxAlert").className = "";
            return false;
        }
        document.getElementById("flag").value = 0;
        document.getElementById("subForm").submit();
    }
}

function unsubSubmitCheck() {
    if(emailValidtor()){
        document.getElementById("subForm").submit();
    }
}
