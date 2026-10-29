

import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json'
  }
})

// attach jwt token to api requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')

  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }

  return config
})

// authentication
export const registerUser = (data) =>
  api.post('/auth/register', data)

export const loginUser = (data) =>
  api.post('/auth/login', data)

// onboarding
export const getOnboardingTasks = () =>
  api.get('/onboarding/')

export const createOnboardingTask = (data) =>
  api.post('/onboarding/', data)

export const completeOnboardingTask = (id) =>
  api.patch(`/onboarding/${id}/complete`)

export const getOnboardingProgress = () =>
  api.get('/onboarding/progress')

// resignations
export const submitResignation = (data) =>
  api.post('/resignations/', data)

export const getResignations = () =>
  api.get('/resignations/')

export const updateResignationStatus = (id, status) =>
  api.patch(`/resignations/${id}/status`, { status })

// announcements
export const getAnnouncements = () =>
  api.get('/announcements/')

export const createAnnouncement = (data) =>
  api.post('/announcements/', data)

export const deleteAnnouncement = (id) =>
  api.delete(`/announcements/${id}`)

// tasks
export const getTasks = () =>
  api.get('/tasks/')

export const createTask = (data) =>
  api.post('/tasks/', data)

export const updateTaskStatus = (id, status) =>
  api.patch(`/tasks/${id}/status`, { status })

export const deleteTask = (id) =>
  api.delete(`/tasks/${id}`)

// integrations
export const sendEmail = (recipient, subject, message) =>
  api.post('/integrations/email', null, {
    params: { recipient, subject, message }
  })

export const exportTasksCsv = () =>
  api.get('/integrations/export/tasks/csv', {
    responseType: 'blob'
  })

export const exportTasksPdf = () =>
  api.get('/integrations/export/tasks/pdf', {
    responseType: 'blob'
  })

export const getIntegrationStatus = () =>
  api.get('/integrations/status')

export const syncCalendar = () =>
  api.post('/integrations/calendar/sync')

// feedback
export const submitFeedback = (data) =>
  api.post('/feedback/', data)

export const getAllFeedback = () =>
  api.get('/feedback/')

export const getMyFeedback = () =>
  api.get('/feedback/my')

// profile and settings
export const getProfile = () =>
  api.get('/profile/')

export const updateProfile = (data) =>
  api.put('/profile/', data)

export const changePassword = (data) =>
  api.post('/profile/change-password', data)

export const getPreferences = () =>
  api.get('/profile/preferences')

export const updatePreferences = (data) =>
  api.put('/profile/preferences', data)

export default api
