import zxcvbn from 'zxcvbn'
import { REST_AUTH } from '../actions/restAuth'

const passValidation = store => next => action => {
  switch (action.type) {
    case REST_AUTH.PASSWORD_VALIDATE:
      const password = action.payload.target.value
      const evaluate = zxcvbn(password)
      action.payload = evaluate
      return next(action)
    default:
      return next(action)
  }
}

export default passValidation