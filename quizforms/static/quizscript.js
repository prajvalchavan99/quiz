function toggleAddQuestion() {
  var addQuestionSection = document.getElementById('addQuestionSection');
  var addQuestionIcon = document.getElementById('addQuestionIcon');
  if (addQuestionSection.classList.contains("show")) {
    addQuestionSection.classList.remove("show");
    addQuestionIcon.classList.remove("fa-minus");
    addQuestionIcon.classList.add("fa-plus");
  } else {
    addQuestionSection.classList.add("show");
    addQuestionIcon.classList.remove("fa-plus");
    addQuestionIcon.classList.add("fa-minus");
  }
}
function confirmDeleteQuiz(id) {
  var confirmDelete = confirm("Are you sure you want to delete quiz " + id + "?")
  if (confirmDelete) {
    console.log("deleted");
  }
}

function showSettings(section) {
  var settingsGroups=document.getElementsByClassName('quiz-group');
  for (let i = 0; i < settingsGroups.length; i++) {
    settingsGroups[i].style.display="none";
  }

  var selectedSettingGroup = document.getElementById(section + '-settings');
  selectedSettingGroup.style.display="block";

  var sidebarItems = document.getElementsByClassName('quiz-sidebar-item');
  for (let i = 0; i < sidebarItems.length; i++) {
    sidebarItems[i].classList.remove("active");
  }

  var selectedSidebarItem = document.querySelector('quiz-sidebar-item[data-section="'+ section +'"]');
  selectedSidebarItem.classList.add('active')
}

function showMessage(message, type) {
  var messageElement = null;
  if (type === 'success') {
      messageElement = document.getElementById('success-message');
  } else if (type === 'error') {
      messageElement = document.getElementById('error-message');
  }

  if (messageElement) {
      messageElement.textContent = message;
      messageElement.classList.add('show');
      // messageElement.style.display="block";
      setTimeout(function() {
          messageElement.classList.remove('show');
      }, 5000);
  }
}

function updateContent(id,element){
  document.getElementById("textarea-"+id).value=element.innerHTML;
}

function slugifyQuizTitle(value){
  var slugifyString = value.toString().toLowerCase()
    .replace(/\s+/g, '-')
    .replace(/&/g, '-and-')
    .replace(/[^\w\-]+/g, '')
    .replace(/\-\-+/g, '-')
    .replace(/^-+/, '')
    .replace(/-+$/, '')

  document.getElementById("id_quizslug").value=slugifyString;
}