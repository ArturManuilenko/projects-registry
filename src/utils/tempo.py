from datetime import datetime, timedelta
from typing import Dict, Any, Optional, Union, List
from requests.exceptions import HTTPError
from src.vendor.tempo_sdk.tempoapiclient import client
import src.conf.tempo_api as tempo_conf


class TempoException(HTTPError):
    pass


class Tempo():
    __client = None
    request_count = 0

    def __init__(self) -> None:
        try:
            self.__client = client.Tempo(
                base_url=tempo_conf.SERVER,
                auth_token=tempo_conf.TOKEN
            )
            self.request_count += 1
        except HTTPError as e:
            raise TempoException(e.args[0])

    def _format_list_responce(self, response: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        result = []
        for resp in response:
            if resp.get('startDate', None):
                start_date = datetime.strptime(resp['startDate'], "%Y-%m-%d").strftime('%d.%m.%Y')
                end_date = datetime.strptime(resp['startDate'], "%Y-%m-%d").strftime('%d.%m.%Y')
            else:
                end_date, start_date = None, None
            if resp.get('startTime', None) and resp.get('timeSpentSeconds', None):
                work_time = timedelta(seconds=float(resp['timeSpentSeconds']))
                end_time = str((datetime.strptime(resp['startTime'], '%H:%M:%S') + work_time).time())
            else:
                end_time = None
            result.append({
                'user_id': resp['author']['accountId'],
                'task_key': resp['issue']['key'] if resp.get('issue', None) else None,
                'description': resp['description'] if resp.get('description', None) else None,
                'start_date': start_date,
                'start_time': resp['startTime'] if resp.get('startTime', None) else None,
                'end_date': end_date,
                'end_time': end_time
            })
        return result

    def _format_dict_result(self, response: Dict[str, Any]) -> Dict[str, Any]:
        if response.get('startDate', None):
            start_date = datetime.strptime(response['startDate'], "%Y-%m-%d").strftime('%d.%m.%Y')
            end_date = datetime.strptime(response['startDate'], "%Y-%m-%d").strftime('%d.%m.%Y')
        else:
            end_date, start_date = None, None
        if response.get('startTime', None) and response.get('timeSpentSeconds', None):
            work_time = timedelta(seconds=float(response['timeSpentSeconds']))
            end_time = str((datetime.strptime(response['startTime'], '%H:%M:%S') + work_time).time())
        else:
            end_time = None
        return {
            'user_id': response['author']['accountId'],
            'task_key': response['issue']['key'] if response.get('issue', None) else None,
            'description': response['description'] if response.get('description', None) else None,
            'start_date': start_date,
            'start_time': response['startTime'] if response.get('startTime', None) else None,
            'end_date': end_date,
            'end_time': end_time
        }

    def _format_result(self, response: Union[List[Any], Dict[str, Any]]) -> Union[List[Dict[str, Any]], Dict[str, Any]]:
        """ Method for get only needed values from API Tempo response """
        if isinstance(response, dict):
            return self._format_dict_result(response)
        elif isinstance(response, list):
            return self._format_list_responce(response)

    def get_user_worklogs(
        self,
        user_id: str,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None
    ) -> Union[List[Dict[str, Any]], Dict[str, Any]]:
        try:
            if from_date and to_date:
                return self._format_result(
                    self.__client.get_worklogs(
                        accountId=user_id,
                        dateFrom=datetime.strptime(from_date, '%d.%m.%Y').date(),
                        dateTo=datetime.strptime(to_date, '%d.%m.%Y').date()
                    )
                )
            else:
                return self._format_result(self.__client.get_worklogs(accountId=user_id))
        except HTTPError as e:
            raise TempoException(e.args[0])

    def get_issue_worklogs(
        self,
        issue_id: str,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None
    ) -> Union[List[Dict[str, Any]], Dict[str, Any]]:
        try:
            if from_date and to_date:
                return self._format_result(
                    self.__client.get_worklogs(
                        issueId=issue_id,
                        dateFrom=datetime.strptime(from_date, '%d.%m.%Y').date(),
                        dateTo=datetime.strptime(to_date, '%d.%m.%Y').date()
                    )
                )
            else:
                return self._format_result(self.__client.get_worklogs(issueId=issue_id))
        except HTTPError as e:
            raise TempoException(e.args[0])
        except ValueError as e:
            raise TempoException(e.args[0])

    def get_project_worklogs(
        self,
        project_key: str,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None
    ) -> Union[List[Dict[str, Any]], Dict[str, Any]]:
        try:
            if from_date and to_date:
                return self._format_result(
                    self.__client.get_worklogs(
                        projectKey=project_key,
                        dateFrom=datetime.strptime(from_date, '%d.%m.%Y').date(),
                        dateTo=datetime.strptime(to_date, '%d.%m.%Y').date()
                    )
                )
            else:
                return self._format_result(
                    self.__client.get_worklogs(projectKey=project_key)
                )
        except HTTPError as e:
            raise TempoException(e.args[0])
