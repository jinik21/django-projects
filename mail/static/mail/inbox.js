document.addEventListener('DOMContentLoaded', function () {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
  document.querySelector('#compose-form').onsubmit = (event) => send_email(event);

});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}
function load_mailbox(mailbox) {

  // Show the mailbox and hide other views
  document.querySelector('#message').style.display = 'none';
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';



  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  fetch(`/emails/${mailbox}`)
    .then(response => response.json())
    .then(response => {
      console.log(response);
      const hd = document.createElement('div');
      if (mailbox == 'sent') {
        hd.innerHTML = `
      <div class="table-responsive" ng-show="!isMessageSelected()">
      <table class="table table-hover refresh-container pull-down">
          <thead class="hidden-xs">
          <tr>
              <td class="col-sm-2"><a href="javascript:;"><strong>To</strong></a></td>
              <td class="col-sm-4"><a href="javascript:;"><strong>Subject</strong></a></td>
              <td class="col-sm-3"><a href="javascript:;"><strong>Date</strong></a></td>
          </tr>
          </thead>
          <tbody id="t-body-email">
          </tbody>
      </table>
  </div>`;
      }
      else {
        hd.innerHTML = `
      <div class="table-responsive" ng-show="!isMessageSelected()">
      <table class="table table-hover refresh-container pull-down">
          <thead class="hidden-xs">
          <tr>
              <td class="col-sm-2"><a href="javascript:;"><strong>From</strong></a></td>
              <td class="col-sm-4"><a href="javascript:;"><strong>Subject</strong></a></td>
              <td class="col-sm-3"><a href="javascript:;"><strong>Date</strong></a></td>
          </tr>
          </thead>
          <tbody id="t-body-email">
          </tbody>
      </table>
  </div>`;
      }
      document.querySelector('#emails-view').append(hd);
      response.forEach(email => {
        const element = document.createElement('tr');
        if (email.read === true)
          element.classList.add("table-secondary");
        if (mailbox == 'sent') {
          element.innerHTML = `
              <td class="col-sm-2 col-xs-4" ">${email.recipients}</td>
              <td class="col-sm-4 col-xs-6" ">${email.subject}</td>
              <td class="col-sm-3 col-xs-4" ">${email.timestamp}</td>
            `;
        }
        else {
          if (email.read == false) {
            element.innerHTML = `
                  <td class="col-sm-2 col-xs-4" "><strong>${email.sender}</strong></td>
                  <td class="col-sm-4 col-xs-6" "><strong>${email.subject}</strong></td>
                  <td class="col-sm-3 col-xs-4" "><strong>${email.timestamp}</strong></td>
                `;
          }
          else {
            element.innerHTML = `
              <td class="col-sm-2 col-xs-4" ">${email.sender}</td>
              <td class="col-sm-4 col-xs-6" ">${email.subject}</td>
              <td class="col-sm-3 col-xs-4" ">${email.timestamp}</td>
            `;
          }
        }
        element.addEventListener("click", () => {
          show_mail(email.id,mailbox);
        });
        document.querySelector('#t-body-email').append(element);
      });
    })
}
function show_mail(id,mailbox) {
  fetch(`/emails/${id}`)
    .then((response) => response.json())
    .then((email) => {
      // Print email
      // console.log(email);
      document.querySelector("#emails-view").innerHTML = "";
      var item = document.createElement("div");
      item.className = `card`;
      item.innerHTML = `<div class="card-body" style="white-space: pre-wrap;">
  Sender: ${email.sender}
  Recipients: ${email.recipients}
  Subject: ${email.subject}
  Time: ${email.timestamp}
  <br>${email.body}
      </div>`;
      document.querySelector("#emails-view").appendChild(item);
      if (mailbox == "sent") return;
      let archivemail = document.createElement("btn");
      archivemail.className = `btn btn-primary my-2`;
      archivemail.addEventListener("click", () => {
        archive_mail(id, email.archived);
        if (archivemail.innerText == "Unarchive") archivemail.innerText = "Archive";
        else archivemail.innerText = "Unarchive";
      });
      if (!email.archived) archivemail.textContent = "Archive";
      else archivemail.textContent = "Unarchive";
      document.querySelector("#emails-view").appendChild(archivemail);

      let replymail = document.createElement("btn");
      replymail.className = `btn btn-primary m-2`;
      replymail.textContent = "Reply";
      replymail.addEventListener("click", () => {
        reply_mail(email.sender, email.subject, email.body, email.timestamp);
      });
      document.querySelector("#emails-view").appendChild(replymail);
      read(id);
    });
}
function archive_mail(id, state) {
  fetch(`/emails/${id}`, {
    method: "PUT",
    body: JSON.stringify({
      archived: !state,
    }),
  })
  .then(response=>{
    load_mailbox('inbox');
  });
}

function read(id) {
  fetch(`/emails/${id}`, {
    method: "PUT",
    body: JSON.stringify({
      read: true,
    }),
  });
}
function reply_mail(sender, subject, body, timestamp) {
  compose_email();
  if (!/^Re:/.test(subject)) subject = `Re: ${subject}`;
  document.querySelector("#compose-recipients").value = sender;
  document.querySelector("#compose-subject").value = subject;

  mail_text = `On ${timestamp} ${sender} wrote:\n${body}\n`;

  document.querySelector("#compose-body").value = mail_text;
}

function send_email(event) {
  event.preventDefault();
  const recipients = document.querySelector('#compose-recipients').value;
  const subject = document.querySelector('#compose-subject').value;
  const body = document.querySelector('#compose-body').value;
  console.log("starting email sending request");
  fetch('/emails',
    {
      method: 'POST',
      body: JSON.stringify({
        recipients: recipients,
        subject: subject,
        body: body
      })
    })
    .then(response => response.json())
    .then(resp => {
      if ("message" in resp) {
        load_mailbox('sent');
      }
      if ("error" in resp) {
        document.querySelector('#message').style.display = 'block';
        document.querySelector('#message').innerHTML = resp['error']
      }

    });
  return false;

}
