
function nope(msg,field){
    Swal.fire({
        title: 'Required Field!',
        text: msg,
        icon: 'error',
        confirmButtonText: 'Ok',
        onClose: ()=>{$(field).click();}
      })
}

function validate_training_form(){
    if ($('#radUploadDataset').is(":checked")){
        if($('#fupDataset').val()==""){
            nope('Please select a dataset to upload or use one of the available ones!','#fupDataset');
            return false
        }
        if($('#txtDatasetName').val()==""){
            nope('Please add a description for the dataset!','#txtDatasetName');
            return false
        }
    }
    if ($('#radLabelUpload').is(":checked")){
        if($('#fupLabel').val()==""){
            nope('Please select a label file to upload or use one of the available ones!','#fupLabel');
            return false
        }
        if($('#txtLabelName').val()==""){
            nope('Please add a description for the label file!','#txtLabelName');
            return false
        }
    }
    if($('#txtDescription').val()==""){
        nope('Please add a meaningful description to your model!','#txtDescription');
        return false
    }
}