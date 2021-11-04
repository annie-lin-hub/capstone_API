const DisplayContainer = document.getElementById('Display');
const enter = document.getElementById('enter');

let myForm = document.forms.namedItem('ProfileForm')
myForm.addEventListener('submit', function(event){
  post_items(event, myForm)
})

DisplayContainer.style = 'display: none'

function post_items (event, form){
  event.preventDefault()

  // let id = document.querySelector('.Student_id').value
  // let name = document.querySelector('.Student_name').value
  // let email = document.querySelector('.Email').value
  // let department = document.querySelector('.Department').value
  // let file = document.querySelector('.jpg').value

  let id = $('.Student_id').val()

  let param = "http://IP:5055/Get?Student_id="+id
    fetch(param,{
        method: 'GET',
        headers: {
        'Accept': 'application/json, text/plain',
        'Content-Type': 'application/json'
        }
    }).then(response => {
        return response.json()
    }) 
    .then( (data) =>{
        render(data)
    })
}

function render(data){
    DisplayContainer.style = 'display: block'
    enter.style = 'display: none'

    let Student_id = data.Student_id;
    let Student_name = data.Student_name;
    let Email = data.Email;
    let Department = data.Department;
    let jpg = data.Picture;

    document.getElementById('Student_id').innerHTML = Student_id;
    document.getElementById('Student_name').innerHTML = Student_name;
    document.getElementById('Email').innerHTML = Email;
    document.getElementById('Department').innerHTML = Department;
    document.getElementById('jpg').innerHTML = '<img src="data:image/jpg;base64, '+ jpg +'" id="jpg" alt="Red dot" />'


}

