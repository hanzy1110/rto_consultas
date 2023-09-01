((nil . (
  (ssh-deploy-root-remote . "/ssh:central_mysql:/home/ubuntu/git/rto_consultas/db_build")
  (ssh-deploy-async . 1)
  (ssh-deploy-async-with-threads . 1)
  (ssh-deploy-on-explicit-save . 1)
  ;; (ssh-deploy-script . (lambda() (let ((default-directory ssh-deploy-root-remote)) (shell-command "bash compile.sh"))))
)))
