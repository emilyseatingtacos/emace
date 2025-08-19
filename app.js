const days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
const quotes = {
  Sunday: "Rest and recharge for the week ahead.",
  Monday: "Start strong, finish stronger.",
  Tuesday: "Keep going, you're doing great.",
  Wednesday: "Halfway there, stay focused.",
  Thursday: "Push through, the weekend is near.",
  Friday: "Finish the week with a win.",
  Saturday: "Enjoy the journey, rest and play."
};

const now = new Date();
const dayName = days[now.getDay()];
document.body.classList.add(dayName.toLowerCase());

document.getElementById('greeting').textContent = `${dayName} Motivation`;
document.getElementById('date').textContent = now.toDateString();
document.getElementById('quote').textContent = quotes[dayName];

if ('geolocation' in navigator) {
  navigator.geolocation.getCurrentPosition(async position => {
    const { latitude, longitude } = position.coords;
    const url = `https://api.open-meteo.com/v1/forecast?latitude=${latitude}&longitude=${longitude}&current_weather=true`;
    try {
      const response = await fetch(url);
      const data = await response.json();
      const temp = data.current_weather.temperature;
      const wind = data.current_weather.windspeed;
      document.getElementById('weather').textContent = `${temp}°C, wind ${wind} km/h`;
    } catch (err) {
      document.getElementById('weather').textContent = 'Unable to fetch weather.';
    }
  }, () => {
    document.getElementById('weather').textContent = 'Location permission denied.';
  });
} else {
  document.getElementById('weather').textContent = 'Geolocation not supported.';
}
