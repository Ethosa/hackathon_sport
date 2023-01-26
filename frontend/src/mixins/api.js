import { userStore } from "@/store";
import axios from "axios";
/**
 * Provides working around API
 */

const API_URL = "http://localhost:8000/";

async function getUser(userId) {
  const response = await fetch(`${API_URL}user${userId}`);
  return await response.json();
}

async function getTask(solutionId) {
  const response = await fetch(`${API_URL}task${solutionId}`);
  return await response.json();
}

async function getAllTasks() {
  const response = await fetch(`${API_URL}tasks`);
  return await response.json();
}

async function getLang(langId) {
  const response = await fetch(`${API_URL}lang${langId}`);
  return await response.json();
}

async function getAllLangs() {
  const response = await fetch(`${API_URL}langs`);
  return await response.json();
}

async function getRole(roleId) {
  const response = await fetch(`${API_URL}role${roleId}`);
  return await response.json();
}

async function getAllRoles() {
  const response = await fetch(`${API_URL}roles`);
  return await response.json();
}

async function getMark(markId) {
  const response = await fetch(`${API_URL}mark${markId}`);
  return await response.json();
}

async function sendSolution(code, task_id, lang, token = userStore().token) {
  const response = await axios
      .put(`${API_URL}solution`, {
        code: code,
        access_token: token,
        task_id: task_id,
        lang: lang,
      })
      .then((res) => {
        return res.data.response ? res.data.response : res.data;
      })
      .catch((err) => {
        return err;
      });
  return await response;
}

async function auth(login, password) {
  const response = await fetch(
      `${API_URL}auth?login=${login}&password=${password}`
  );
  return await response.json();
}

async function register(login, password, fullName, group) {
  const response = await fetch(`${API_URL}user`, {
    method: "POST",
    body: JSON.stringify({
      name: fullName,
      login: login,
      password: password,
      group: group,
    }),
  });
  return await response.json();
}

const API = {
  auth,
  getAllTasks,
  getMark,
  getTask,
  getUser,
  register,
  getRole,
  getAllRoles,
  getLang,
  getAllLangs,
  sendSolution,
};

export default API;