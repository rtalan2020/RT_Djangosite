getthoughts();
function getthoughts(){
var number = Math.floor(Math.random() * 1643)
var thoughts = document.getElementById('thoughts');
var p_author = document.createElement('p');
if (thoughts != null){
fetch('https://type.fit/api/quotes')
  .then(function (response) {
    return response.json();
  })
  .then(function (data) {
    thoughts.innerHTML = data[number].text;
    p_author.innerHTML = data[number].author;
    p_author.classList.add('thought_author');
    thoughts.appendChild(p_author);
  })
  .catch(function (err) {
    console.log(err);
  });
}
}

// $('#exampleModal').on('show.bs.modal', function (event) {
//   var button = $(event.relatedTarget) // Button that triggered the modal
//   var recipient = button.data('whatever') // Extract info from data-* attributes
//   // If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
//   // Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
//   recipient =   recipient.toUpperCase();
//   var modal = $(this)
//   modal.find('.modal-title').text('Hi ' + recipient + ", Time for Video Feature Change")
//   // modal.find('.modal-body input').val(recipient)
// })


function getVideo(src, title, description){
  var youtube = document.getElementById('youtube_src');
  var v_title = document.getElementById('video_title');
  var v_description = document.getElementById('video_description');

  youtube.innerHTML = "https://www.youtube.com/embed/_uQrJ0TkZlc" + src;
  v_title.innerHTML = title;
  v_description.innerHTML = description;

}

var sel = document.getElementById('selectid');
var realSearchValue = document.getElementById('realSearchValue');
// transfer()

function transfer(){
  var searchhidden = document.getElementById('searchhidden');
  var searchhiddenOp = document.getElementById('searchhiddenOp');
  searchhiddenOp.value=realSearchValue.value;
  searchhidden.value = sel.value;
}

function pformSubmit(){
  var perpageForm = document.getElementById('perpageSubmit');
  perpageForm.submit();
  
}



