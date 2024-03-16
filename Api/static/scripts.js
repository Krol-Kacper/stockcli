const input = document.getElementById("input");
const select_1 = document.getElementById("select1");
const select_2 = document.getElementById("select2");

async function getCurrencies() {
  const data = await (await fetch("/cli/list")).json();
  const keys = Object.keys(data);

  let index = keys.indexOf("updated");
  keys.splice(index, 1);
  index = keys.indexOf("BTC");
  keys.splice(index, 1);
  for(let i=0; i<keys.length; i++){
    const opt_1 = document.createElement("option");
    const opt_2 = document.createElement("option");
    opt_1.innerText = keys[i];
    opt_1.value = keys[i];
    opt_2.innerText = keys[i];
    opt_2.value = keys[i];
    select_1.appendChild(opt_1);
    select_2.appendChild(opt_2);
  }
}
async function getRequest(value, start, end){
  const query = "start="+start+"&value="+value+"&end="+end;
  const response = await (await fetch("/cli/cli?"+query)).json();
  return response
}

function updateTime() {
  const now = new Date();
  const hour = now.getHours();
  const minute = now.getMinutes();

  document.getElementById('time').innerText = hour + ':' + (minute < 10 ? '0' + minute : minute);
  requestAnimationFrame(updateTime);
}

function onInput(){
  const input = document.getElementById("input");
  const output = document.getElementById("output");
  const val = input.value;
  const intval = parseFloat(val);
  if (!isNaN(intval)){
    from = select_1.value;
    to = select_2.value;
    getRequest(intval, from, to, 2)
    .then(response => {
      output.value = response
    })
  }
} 

select_1.onchange = onInput;
select_2.onchange = onInput;
input.oninput = onInput;
updateTime();
getCurrencies();
