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
  const defenders = team.filter(player => player.position === 'Defender')
  const midfielders = team.filter(player => player.position === 'Midfielder')
  const forwards = team.filter(player => player.position === 'Attacker')

  const lineUp = new Map()
  lineUp.set('goalkeepers', [goalkeepers[0]])
  lineUp.set('defenders', defenders.slice(0, formationArr[0]))
  lineUp.set('midfielders', midfielders.slice(0, formationArr[1]))
  lineUp.set('attackers', forwards.slice(0, formationArr[2]))
  lineUp.set(
    'substitutes',
    team.filter(
      player =>
        !lineUp.get('goalkeepers').includes(player) &&
        !lineUp.get('defenders').includes(player) &&
        !lineUp.get('midfielders').includes(player) &&
        !lineUp.get('attackers').includes(player)
    )
  )

  return lineUp
}
