function loadTemplateAsync(path) {
  const result = new Promise(resolve => {
    const xhttp = new XMLHttpRequest()

    xhttp.onreadystatechange = function () {
      if (this.readyState == 4) {
        if (this.status == 200) resolve(this.responseText)

        if (this.status == 404) resolve(`<div>Page not found: ${path}</div>`)
      }
    }

    xhttp.open('GET', path, true)
    xhttp.send()
  })

  return result
}

function constructLineUp(formation, team) {
  const formationArr = formation.split('-').map(Number)
  const goalkeepers = team.filter(player => player.position === 'Goalkeeper')
  const defenders = team.filter(player => player.position === 'Defence')
  const midfielders = team.filter(player => player.position === 'Midfield')
  const forwards = team.filter(player => player.position === 'Offense')

  const lineUp = new Map()
  lineUp.set('formation', formation)
  lineUp.set('goalkeepers', goalkeepers[0])
  lineUp.set('defenders', defenders.slice(0, formationArr[1] - 1))
  lineUp.set('midfielders', midfielders.slice(0, formationArr[2] - 1))
  lineUp.set('forwards', forwards.slice(0, formationArr[3] - 1))

  console.log(lineUp)

  return lineUp
}
